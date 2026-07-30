"""Finance Agent service.

This module provides the FinanceAgentService which:
1. Receives a business proposal
2. Builds the Finance prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a FinanceAgentResponse object

This service is designed as the reference implementation for all department agents.
"""

import json
import os
import logging
from typing import Optional

from .prompt import FINANCE_SYSTEM_PROMPT, build_finance_prompt
from .schema import FinanceAgentRequest, FinanceAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


# Backward-compatible alias so other agents importing from here still work
LLMProvider = get_provider


class FinanceAgentService:
    """Service for the Finance Agent in Department Workspace mode.

    This class encapsulates the complete Finance Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = FinanceAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: FinanceAgentRequest) -> FinanceAgentResponse:
        """Analyze a business proposal from the CFO perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated FinanceAgentResponse with complete financial analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_finance_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for Finance Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="finance",
            llm_generate=self.llm.generate,
            system_prompt=FINANCE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> FinanceAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated FinanceAgentResponse.

        Raises:
            ValueError: If parsing or validation fails.
        """
        # Strip markdown code fences if present
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove first line (```json) and last line (```)
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM response is not valid JSON: {e}")

        # Ensure agent_id is correct
        data["agent_id"] = "finance"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return FinanceAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: FinanceAgentRequest) -> FinanceAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response. When MCP evidence
        is present, it references the uploaded data.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "finance")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["reduce", "cut", "optimize", "save"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["expensive", "risky", "uncertain", "unproven"]):
            position = "oppose"
            confidence = 0.7
        elif any(word in scenario_lower for word in ["invest", "expand", "launch", "grow"]):
            position = "conditional"
            confidence = 0.6
        else:
            position = "neutral"
            confidence = 0.5

        # Determine risk level
        if any(word in scenario_lower for word in ["million", "enterprise", "international"]):
            risk_level = "high"
        elif any(word in scenario_lower for word in ["pilot", "small", "test"]):
            risk_level = "low"
        else:
            risk_level = "medium"

        # Build evidence-aware domain assessment
        revenue_impact = (
            f"Based on uploaded data: ${facts['total_revenue']} total projected revenue. "
            f"Highest contributor: {facts.get('top_performer', 'N/A')}. "
            f"Growth range: {facts.get('min_growth', 'N/A')} to {facts.get('max_growth', 'N/A')}."
        ) if facts.get("has_evidence") and facts.get("total_revenue") else (
            "Estimated revenue impact requires further quantification. "
            "Based on the proposal scope, potential range is $500K-$2M "
            "annually depending on execution and market conditions."
        )

        return FinanceAgentResponse(
            agent_id="finance",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "revenue_impact": revenue_impact,
                "cost_impact": (
                    "Direct costs estimated at $300K-$800K for initial implementation. "
                    "Ongoing operational costs of $50K-$150K/month depending on scale. "
                    "Hidden costs likely include integration, training, and opportunity cost."
                ),
                "roi_estimate": (
                    "Projected ROI of 80-150% over 24 months, assuming successful execution. "
                    "Key assumption: revenue projections are achievable within stated timeline. "
                    "Sensitivity: 20% revenue shortfall reduces ROI to 40-90%."
                ),
                "payback_period": (
                    "Estimated 12-18 months to break-even on fully-loaded cost basis. "
                    "Best case: 10 months with accelerated adoption. "
                    "Worst case: 24+ months if market conditions deteriorate."
                ),
                "risk_level": risk_level,
            },
            summary=(
                f"From a CFO perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — the financial case requires "
                f"validation of key revenue assumptions before full commitment."
            ),
            rationale=(
                evidence_prefix +
                "From a pure financial standpoint, this proposal presents a "
                "reasonable risk-reward profile that warrants careful consideration. "
                "The projected returns, if achievable, would justify the capital "
                "allocation. However, several assumptions underlying the financial "
                "model require validation.\n\n"
                "The cost structure appears manageable relative to our current "
                "financial position, but I note that the implementation timeline "
                "creates a significant cash exposure period before revenue "
                "realization. During this period, we are deploying capital without "
                "a proven return, which must be weighed against alternative uses "
                "of that capital.\n\n"
                "I recommend a staged approach: authorize an initial phase with "
                "defined success criteria before committing the full investment. "
                "This limits downside exposure while preserving the upside "
                "opportunity. The financial thresholds for proceeding to full "
                "investment should be agreed upon upfront."
            ),
            risks=[
                "Revenue projections are based on unvalidated assumptions — actual results may fall 20-40% below plan",
                "Cash flow gap between investment and revenue creates liquidity pressure during implementation",
                "Opportunity cost: capital deployed here cannot fund other initiatives with potentially higher ROI",
                "Implementation timeline risk — delays increase burn without corresponding revenue offset",
            ],
            conditions=[
                "Validate core revenue assumptions with pilot data before authorizing full investment",
                "Maintain minimum 12 months cash runway at all times during implementation",
                "Establish stage gates with clear financial criteria for continued funding",
                "Cap total initial investment at defined threshold with formal review for additional allocation",
            ],
            metrics_to_track=[
                "Monthly burn rate vs. plan — flag deviations above 15%",
                "Revenue pipeline conversion rate — target validation within first 90 days",
                "Customer acquisition cost (CAC) relative to lifetime value (LTV)",
                "Time to break-even — track monthly against 18-month target",
                "Cash runway months — maintain above 12-month minimum at all times",
            ],
            references_to=[],
        )
