"""Strategy Agent service.

This module provides the StrategyAgentService which:
1. Receives a business proposal
2. Builds the Strategy prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a StrategyAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import STRATEGY_SYSTEM_PROMPT, build_strategy_prompt
from .schema import StrategyAgentRequest, StrategyAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class StrategyAgentService:
    """Service for the Strategy Agent in Department Workspace mode.

    This class encapsulates the complete Strategy Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = StrategyAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: StrategyAgentRequest) -> StrategyAgentResponse:
        """Analyze a business proposal from the CSO perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated StrategyAgentResponse with complete strategic analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_strategy_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for Strategy Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="strategy",
            llm_generate=self.llm.generate,
            system_prompt=STRATEGY_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> StrategyAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated StrategyAgentResponse.

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
        data["agent_id"] = "strategy"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return StrategyAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: StrategyAgentRequest) -> StrategyAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "strategy")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["market leader", "first mover", "disrupt", "dominant"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["saturated", "declining", "commoditized", "late entrant"]):
            position = "oppose"
            confidence = 0.7
        elif any(word in scenario_lower for word in ["expand", "acquire", "partner", "enter"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine strategic priority
        if any(word in scenario_lower for word in ["transform", "pivot", "existential", "critical"]):
            strategic_priority = "critical"
        elif any(word in scenario_lower for word in ["competitive", "growth", "scale", "market share"]):
            strategic_priority = "high"
        elif any(word in scenario_lower for word in ["pilot", "explore", "test", "evaluate"]):
            strategic_priority = "low"
        else:
            strategic_priority = "medium"

        return StrategyAgentResponse(
            agent_id="strategy",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "market_opportunity": (
                    "The addressable market shows moderate-to-strong growth potential. "
                    "Estimated TAM of $2-5B with a realistic serviceable segment of $300-800M. "
                    "Market growth trajectory suggests 12-20% CAGR over the next 3-5 years."
                ),
                "competitive_advantage": (
                    "Current positioning provides a defensible but not insurmountable advantage. "
                    "Key differentiators include existing customer relationships and domain expertise. "
                    "Sustainable moat requires continued investment in proprietary capabilities."
                ),
                "strategic_fit": (
                    "This initiative aligns with the company's stated growth objectives and "
                    "supports the long-term vision of market expansion. Integration with existing "
                    "capabilities is feasible but requires deliberate coordination."
                ),
                "execution_complexity": (
                    "Moderate-to-high execution complexity given the need for new capabilities, "
                    "market relationships, and potential organizational restructuring. "
                    "Estimated 12-18 months to achieve strategic milestones."
                ),
                "strategic_priority": strategic_priority,
            },
            summary=(
                f"From a strategic perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — the market opportunity warrants "
                f"pursuit contingent on competitive positioning validation."
            ),
            rationale=(
                evidence_prefix +
                "From a strategic standpoint, this proposal addresses a meaningful market "
                "opportunity that aligns with our corporate direction. The competitive "
                "landscape suggests a window of opportunity exists, though it requires "
                "decisive action to capitalize on before market dynamics shift.\n\n"
                "The strategic fit with our current capabilities and vision is reasonable, "
                "but success depends on our ability to build or acquire complementary "
                "capabilities. The execution complexity is manageable if properly resourced "
                "and sequenced, though it requires cross-functional alignment.\n\n"
                "I recommend a phased strategic approach: validate key market assumptions "
                "in Phase 1, build strategic capabilities in Phase 2, and scale aggressively "
                "in Phase 3. Each phase should have clear strategic gates that confirm "
                "market conditions remain favorable before committing additional resources."
            ),
            risks=[
                "Competitive response risk — incumbents may accelerate their roadmaps or engage in price warfare upon market entry",
                "Market timing risk — window of opportunity may close if execution takes longer than 12-18 months",
                "Strategic dilution — pursuing this initiative may divert focus from core business at a critical growth stage",
                "Capability gap — required competencies may take longer to build than anticipated, eroding first-mover advantage",
            ],
            conditions=[
                "Validate market demand assumptions through pilot engagement before full commitment",
                "Confirm competitive landscape has not materially shifted before Phase 2 authorization",
                "Ensure strategic initiative does not reduce core business growth below 15% threshold",
                "Establish partnership or acquisition pipeline for critical capability gaps within 90 days",
            ],
            metrics_to_track=[
                "Market share capture rate — target 5% of SAM within 24 months",
                "Competitive win rate in target segments — track monthly",
                "Strategic capability readiness score — assess quarterly against plan",
                "Time-to-market vs. competition — maintain first-mover or fast-follower position",
                "Core business growth rate — must remain above 15% during strategic expansion",
            ],
            references_to=[],
        )
