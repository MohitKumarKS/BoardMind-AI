"""CEO Agent service.

This module provides the CEOAgentService which:
1. Receives a business proposal
2. Builds the CEO prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a CEOAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import CEO_SYSTEM_PROMPT, build_ceo_prompt
from .schema import CEOAgentRequest, CEOAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class CEOAgentService:
    """Service for the CEO Agent in Department Workspace mode.

    This class encapsulates the complete CEO Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = CEOAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: CEOAgentRequest) -> CEOAgentResponse:
        """Analyze a business proposal from the CEO perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated CEOAgentResponse with complete strategic analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_ceo_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for CEO Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="ceo",
            llm_generate=self.llm.generate,
            system_prompt=CEO_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> CEOAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated CEOAgentResponse.

        Raises:
            ValueError: If parsing or validation fails.
        """
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM response is not valid JSON: {e}")

        data["agent_id"] = "ceo"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return CEOAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: CEOAgentRequest) -> CEOAgentResponse:
        """Generate a realistic mock response for development and testing.

        Analyzes keywords in the scenario to produce a contextually
        relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "ceo")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["strategic", "vision", "growth", "expand", "market leader"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["distraction", "off-brand", "unfocused", "dilute"]):
            position = "oppose"
            confidence = 0.75
        elif any(word in scenario_lower for word in ["pivot", "transform", "restructure", "acquire"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine risk level
        if any(word in scenario_lower for word in ["pivot", "acquisition", "international", "restructure"]):
            risk_level = "high"
        elif any(word in scenario_lower for word in ["pilot", "incremental", "extension"]):
            risk_level = "low"
        else:
            risk_level = "medium"

        return CEOAgentResponse(
            agent_id="ceo",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "strategic_alignment": (
                    "This proposal aligns with our stated strategic priorities "
                    "around growth and market expansion. It directly supports our "
                    "3-year vision of category leadership and addresses a clear "
                    "market opportunity within our core competency zone."
                ),
                "stakeholder_impact": (
                    "Shareholders benefit from accelerated growth trajectory. "
                    "Employees face moderate change management requirements but gain "
                    "career development opportunities. Customers receive enhanced "
                    "value proposition. Partner ecosystem may require realignment."
                ),
                "competitive_positioning": (
                    "Positions us favorably against primary competitors by "
                    "addressing an underserved segment. Creates potential "
                    "12-18 month first-mover advantage if executed within the "
                    "proposed timeline. Competitors are likely 6-9 months behind."
                ),
                "execution_priority": (
                    "Recommend P1 priority status with dedicated executive sponsor. "
                    "Market timing suggests action within current quarter to "
                    "capture window of opportunity. Delay risks competitor preemption."
                ),
                "risk_level": risk_level,
            },
            summary=(
                f"As CEO, I view this proposal as {position} — it "
                f"{'advances our strategic vision and market position' if position == 'support' else 'requires careful evaluation against our core strategic priorities'} "
                f"with {confidence:.0%} confidence in this assessment."
            ),
            rationale=(
                evidence_prefix +
                "From a strategic perspective, this proposal addresses a genuine "
                "market opportunity that aligns with our stated corporate direction. "
                "The timing is relevant given competitive dynamics — our window of "
                "advantage is finite and the cost of inaction must be weighed "
                "against the cost of execution.\n\n"
                "Stakeholder alignment is achievable but requires proactive "
                "communication. The board will need to see a clear connection "
                "between this initiative and our 3-year strategic plan. Employees "
                "will need clarity on how this fits within existing priorities to "
                "avoid initiative fatigue. Customer impact should be framed as "
                "value expansion rather than disruption.\n\n"
                "My primary concern is execution focus — we must ensure this does "
                "not dilute our core business momentum. I would authorize this "
                "initiative only with a dedicated execution team that does not "
                "draw from critical ongoing projects. The strategic upside "
                "justifies the investment if we maintain disciplined execution."
            ),
            risks=[
                "Strategic dilution — spreading organizational focus across too many initiatives reduces execution quality on core business",
                "Market timing risk — if execution takes longer than 6 months, competitive window may narrow significantly",
                "Stakeholder misalignment — board expectations and operational reality may diverge without clear milestone communication",
                "Organizational capacity — current team may lack bandwidth to absorb new strategic initiative without performance degradation",
            ],
            conditions=[
                "Dedicated execution team that does not pull from critical existing projects",
                "Board-approved strategic alignment document connecting this to 3-year plan",
                "Clear 90-day milestone plan with executive review checkpoints",
                "Defined success criteria and kill switch thresholds agreed upon before launch",
            ],
            metrics_to_track=[
                "Strategic initiative progress vs. 90-day milestone plan",
                "Core business performance — must not degrade more than 5% during execution",
                "Competitive position tracking — quarterly market share assessment",
                "Stakeholder satisfaction scores — board, employee, customer NPS",
                "Time-to-market vs. competitive benchmark",
            ],
            references_to=[],
        )
