"""Customer Success Agent service.

This module provides the CustomerSuccessAgentService which:
1. Receives a business proposal
2. Builds the Customer Success prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a CustomerSuccessAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import CUSTOMER_SUCCESS_SYSTEM_PROMPT, build_customer_success_prompt
from .schema import CustomerSuccessAgentRequest, CustomerSuccessAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class CustomerSuccessAgentService:
    """Service for the Customer Success Agent in Department Workspace mode.

    This class encapsulates the complete Customer Success Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = CustomerSuccessAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: CustomerSuccessAgentRequest) -> CustomerSuccessAgentResponse:
        """Analyze a business proposal from the CCusO perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated CustomerSuccessAgentResponse with complete customer analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_customer_success_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for Customer Success Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="customer_success",
            llm_generate=self.llm.generate,
            system_prompt=CUSTOMER_SUCCESS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> CustomerSuccessAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated CustomerSuccessAgentResponse.

        Raises:
            ValueError: If parsing or validation fails.
        """
        # Strip markdown code fences if present
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM response is not valid JSON: {e}")

        # Ensure agent_id is correct
        data["agent_id"] = "customer_success"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return CustomerSuccessAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: CustomerSuccessAgentRequest) -> CustomerSuccessAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "customer_success")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["improve experience", "reduce churn", "customer first", "satisfaction"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["migration", "deprecate", "remove", "breaking change"]):
            position = "oppose"
            confidence = 0.75
        elif any(word in scenario_lower for word in ["new feature", "launch", "upgrade", "enhance"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine customer risk
        if any(word in scenario_lower for word in ["mandatory", "breaking", "migration", "remove feature"]):
            customer_risk = "high"
        elif any(word in scenario_lower for word in ["optional", "gradual", "beta"]):
            customer_risk = "low"
        else:
            customer_risk = "medium"

        return CustomerSuccessAgentResponse(
            agent_id="customer_success",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "customer_impact": (
                    "This initiative affects approximately 40-60% of the active customer base. "
                    "Existing workflows will require adaptation, with power users experiencing "
                    "the most disruption. Customer health scores may temporarily decline during "
                    "transition before improving post-adoption."
                ),
                "retention_risk": (
                    "Moderate churn risk estimated at 3-5% incremental churn if change management "
                    "is poorly executed. At-risk cohort: customers with low engagement scores "
                    "who may use this disruption as a switching trigger. Proactive outreach "
                    "to red-zone accounts is critical."
                ),
                "satisfaction_forecast": (
                    "Short-term NPS impact: expected -3 to -5 point dip during first 60 days "
                    "due to change fatigue. Medium-term recovery: +5 to +8 points by month 6 "
                    "as improved experience is realized. Net positive trajectory if transition "
                    "is well-communicated and supported."
                ),
                "support_requirements": (
                    "Anticipate 30-50% spike in support ticket volume for 4-6 weeks post-launch. "
                    "Estimated 2-3 additional support FTEs needed temporarily. Self-service "
                    "documentation and in-app guidance can reduce peak load by 40% if deployed "
                    "proactively."
                ),
                "customer_risk": customer_risk,
            },
            summary=(
                f"From a customer success perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — customer impact requires careful change "
                f"management to protect retention and satisfaction."
            ),
            rationale=(
                evidence_prefix +
                "From a customer success standpoint, this initiative has the potential "
                "to improve long-term customer outcomes, but the transition period "
                "presents meaningful retention risk. Our highest-value customers are "
                "often the most sensitive to changes in their established workflows, "
                "and disruption without adequate support can trigger evaluation of "
                "alternatives.\n\n"
                "The key to protecting customer relationships during this initiative "
                "is proactive communication and high-touch support for at-risk accounts. "
                "Our customer health score data indicates which accounts are most "
                "vulnerable to churn triggers, and these accounts need personalized "
                "transition plans. The support team must be resourced to handle the "
                "inevitable spike in inquiries without degrading response times.\n\n"
                "If executed with proper change management — advance notice, dedicated "
                "migration support, feedback loops, and escalation paths — the long-term "
                "customer outcome is positive. The risk is in the execution, not the "
                "strategy itself. I recommend phased rollout starting with our most "
                "engaged customers who are likely to be early adopters and advocates."
            ),
            risks=[
                "At-risk customers (low health scores) may use transition disruption as a switching trigger — estimated 3-5% incremental churn",
                "Support ticket spike overwhelms team capacity, leading to degraded response times and compounding dissatisfaction",
                "Power users with deeply customized workflows face disproportionate disruption and may become vocal detractors",
                "Communication fatigue: too many change notifications reduce engagement with critical transition messages",
            ],
            conditions=[
                "Deploy proactive outreach to all red-zone accounts (health score < 40) before launch with personalized transition plans",
                "Ensure support team has capacity for 50% ticket volume increase without SLA degradation",
                "Establish customer advisory board feedback loop — minimum 10 enterprise customers providing weekly transition feedback",
                "Achieve 80% customer acknowledgment of change communication before proceeding with rollout",
            ],
            metrics_to_track=[
                "Net Promoter Score (NPS) — weekly tracking, alert if drops more than 5 points",
                "Customer health score distribution — monitor shift from green to yellow/red zones",
                "Churn rate by cohort — compare transition cohort to control, target no more than 2% incremental",
                "Support ticket volume and first-response time — maintain SLA during transition spike",
                "Customer effort score (CES) for transition workflow — target below 3.0 (easy)",
            ],
            references_to=[],
        )
