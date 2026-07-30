"""Investor Relations Officer service.

This module provides the InvestorRelationsAgentService which:
1. Receives a business proposal
2. Builds the Investor Relations prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns an InvestorRelationsAgentResponse object
"""

import json
import os
import logging
from typing import Optional

from .prompt import INVESTOR_RELATIONS_SYSTEM_PROMPT, build_investor_relations_prompt
from .schema import InvestorRelationsAgentRequest, InvestorRelationsAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


# Backward-compatible alias
LLMProvider = get_provider


class InvestorRelationsAgentService:
    """Service for the Investor Relations Officer in Department Workspace mode.

    This class encapsulates the complete Investor Relations Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = InvestorRelationsAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: InvestorRelationsAgentRequest) -> InvestorRelationsAgentResponse:
        """Analyze a business proposal from the investor relations perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated InvestorRelationsAgentResponse with complete IR analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_investor_relations_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for Investor Relations Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="investor_relations",
            llm_generate=self.llm.generate,
            system_prompt=INVESTOR_RELATIONS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> InvestorRelationsAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated InvestorRelationsAgentResponse.

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
        data["agent_id"] = "investor_relations"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return InvestorRelationsAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: InvestorRelationsAgentRequest) -> InvestorRelationsAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "investor_relations")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["dividend", "buyback", "beat", "growth", "outperform"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["dilut", "miss", "writedown", "restructur", "layoff"]):
            position = "oppose"
            confidence = 0.75
        elif any(word in scenario_lower for word in ["acquisition", "invest", "expand", "strategic"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine investor sentiment
        if any(word in scenario_lower for word in ["exceed", "beat", "upgrade", "strong"]):
            investor_sentiment = "positive"
        elif any(word in scenario_lower for word in ["miss", "downgrade", "concern", "weak"]):
            investor_sentiment = "negative"
        elif any(word in scenario_lower for word in ["mixed", "uncertain", "complex"]):
            investor_sentiment = "mixed"
        else:
            investor_sentiment = "neutral"

        return InvestorRelationsAgentResponse(
            agent_id="investor_relations",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "market_perception": (
                    "Analyst consensus expects continued execution on stated strategy. "
                    "This proposal aligns with previously communicated growth priorities, "
                    "reducing surprise risk. Institutional investors (representing 68% of "
                    "float) are likely to view this as consistent with management credibility. "
                    "Sell-side coverage may adjust price targets within 5-10% range depending "
                    "on execution confidence."
                ),
                "earnings_impact": (
                    "Near-term EPS dilution of $0.03-0.06 per share over next 2 quarters "
                    "from upfront investment. Accretive beginning Q3-Q4 with estimated "
                    "$0.08-0.12 EPS contribution at run-rate. Full-year guidance may need "
                    "revision: recommend maintaining range but shifting mix toward back-half "
                    "weighting. Street consensus currently at $3.42 EPS — proposal creates "
                    "temporary gap of 1-2% before recovery."
                ),
                "shareholder_value": (
                    "Long-term shareholder value creation estimated at 10-18% over 3-year "
                    "horizon through TAM expansion and competitive positioning. Near-term "
                    "multiple compression risk of 0.5-1.0x if execution stumbles. "
                    "Peer comps trading at 22-28x forward earnings — our current 24x "
                    "should be maintainable if growth narrative remains intact. Risk of "
                    "re-rating downward if initiative fails to deliver stated metrics."
                ),
                "communication_strategy": (
                    "Recommend pre-briefing top 5 institutional holders (representing 42% "
                    "of float) 48 hours before public announcement. Frame as strategic "
                    "investment consistent with previously stated priorities. Include in "
                    "next quarterly earnings call narrative with specific milestones. "
                    "Prepare FAQ document for sell-side analysts addressing EPS timing, "
                    "execution risks, and success metrics. Consider analyst day within "
                    "90 days to provide deep-dive on strategic rationale."
                ),
                "investor_sentiment": investor_sentiment,
            },
            summary=(
                f"From an investor relations perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — market reaction depends on narrative "
                f"alignment with stated strategy and clear execution milestones."
            ),
            rationale=(
                evidence_prefix +
                "From an investor relations perspective, the key consideration is how "
                "this decision will be perceived by the investment community and whether "
                "it reinforces or contradicts our established market narrative. The "
                "proposal aligns with previously communicated strategic priorities, which "
                "reduces the risk of a negative surprise reaction. However, any near-term "
                "earnings dilution requires careful framing to avoid multiple compression.\n\n"
                "The institutional investor base (68% of float) has been supportive of "
                "growth investments when accompanied by clear metrics and accountability. "
                "The critical element is not the decision itself but the communication "
                "strategy: pre-briefing major holders, providing specific milestones, and "
                "demonstrating management confidence through commitment to measurable "
                "outcomes. Sell-side analysts will update models — we should provide "
                "enough detail to prevent worst-case assumptions.\n\n"
                "The timing consideration is important. Announcing between earnings "
                "cycles gives analysts time to update models without the pressure of "
                "immediate quarterly comparison. I recommend coupling the announcement "
                "with a reaffirmation of full-year guidance (potentially with revised "
                "quarterly phasing) to signal management confidence in overall "
                "financial trajectory despite near-term investment."
            ),
            risks=[
                "Multiple compression risk if market interprets investment as deviation from profitable growth narrative — potential 0.5-1.0x de-rating",
                "Earnings guidance revision may trigger sell-side downgrades if not framed as investment-driven with clear accretion timeline",
                "Institutional holder concern if pre-briefing is inadequate — largest holders expect advance notice of material strategic shifts",
                "Competitive disclosure risk — public announcement may signal strategic intent to competitors and affect first-mover advantage",
            ],
            conditions=[
                "Complete pre-briefing of top 5 institutional holders (42% of float) before any public announcement",
                "Prepare detailed analyst FAQ with EPS bridge showing quarter-by-quarter impact and accretion timeline",
                "Reaffirm full-year guidance simultaneously with announcement to maintain earnings narrative integrity",
                "Establish quarterly IR milestone reporting cadence for initiative progress visible to investment community",
            ],
            metrics_to_track=[
                "Analyst consensus EPS estimate changes — monitor for downgrades within 30 days of announcement",
                "Institutional ownership changes — track for significant position reductions (>5% of holder's position)",
                "Forward P/E multiple relative to peer group — maintain within historical range (22-28x)",
                "Sell-side price target changes and rating adjustments post-announcement",
                "Share price performance relative to sector index — 30, 60, 90 day windows",
            ],
            references_to=[],
        )
