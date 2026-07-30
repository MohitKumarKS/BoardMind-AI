"""Product Agent service.

This module provides the ProductAgentService which:
1. Receives a business proposal
2. Builds the Product prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a ProductAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import PRODUCT_SYSTEM_PROMPT, build_product_prompt
from .schema import ProductAgentRequest, ProductAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class ProductAgentService:
    """Service for the Product Agent in Department Workspace mode.

    This class encapsulates the complete Product Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = ProductAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: ProductAgentRequest) -> ProductAgentResponse:
        """Analyze a business proposal from the CPO perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated ProductAgentResponse with complete product analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_product_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for Product Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="product",
            llm_generate=self.llm.generate,
            system_prompt=PRODUCT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> ProductAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated ProductAgentResponse.

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
        data["agent_id"] = "product"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return ProductAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: ProductAgentRequest) -> ProductAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "product")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["user demand", "validated", "top request", "high nps"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["no research", "unvalidated", "low usage", "bloat"]):
            position = "oppose"
            confidence = 0.7
        elif any(word in scenario_lower for word in ["feature", "launch", "build", "add"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine feasibility
        if any(word in scenario_lower for word in ["simple", "quick", "minor", "tweak"]):
            feasibility = "straightforward"
        elif any(word in scenario_lower for word in ["impossible", "unrealistic", "years"]):
            feasibility = "infeasible"
        elif any(word in scenario_lower for word in ["complex", "overhaul", "rewrite", "platform"]):
            feasibility = "complex"
        else:
            feasibility = "moderate"

        return ProductAgentResponse(
            agent_id="product",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "product_market_fit": (
                    "Initial signals suggest moderate product-market fit potential. "
                    "User interviews and competitive analysis indicate demand exists, "
                    "but depth of need requires validation through prototype testing. "
                    "Recommend user research sprint before full commitment."
                ),
                "roadmap_impact": (
                    "This initiative would require reprioritizing Q3-Q4 roadmap items. "
                    "Estimated displacement: 2-3 planned features delayed by one quarter. "
                    "The trade-off is acceptable if user validation confirms strong demand, "
                    "but creates commitment debt on existing customer promises."
                ),
                "user_experience": (
                    "User journey impact is moderate — adds a new workflow path that "
                    "must integrate seamlessly with existing navigation patterns. "
                    "Onboarding complexity increases slightly but long-term usability "
                    "improves if executed well. A/B testing recommended during rollout."
                ),
                "build_vs_buy": (
                    "Build recommended for core differentiating capability. "
                    "Existing vendor solutions address 60% of the need but lack "
                    "deep integration with our existing product architecture. "
                    "Partnership model viable for non-core components."
                ),
                "feasibility": feasibility,
            },
            summary=(
                f"From a product perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — the user need is plausible but "
                f"requires validation before full roadmap commitment."
            ),
            rationale=(
                evidence_prefix +
                "From a product standpoint, this proposal addresses a recognized user "
                "need that aligns with our product vision. Competitive analysis shows "
                "that similar capabilities exist in adjacent products, confirming market "
                "demand. However, our specific user base has not been directly surveyed "
                "on this need, creating a validation gap.\n\n"
                "The roadmap impact is manageable if we approach this as a phased "
                "initiative. I recommend starting with an MVP that tests the core "
                "value proposition with a subset of users before committing engineering "
                "resources to the full vision. This limits roadmap disruption while "
                "generating the user data needed for confident prioritization.\n\n"
                "User experience implications require careful design attention. The "
                "proposed capability adds complexity to the product surface area, which "
                "must be balanced against simplicity — our core UX principle. Progressive "
                "disclosure and smart defaults can mitigate complexity concerns."
            ),
            risks=[
                "User need is inferred from competitive analysis rather than validated through direct research — may be solving the wrong problem",
                "Roadmap displacement creates delivery debt on features already promised to key accounts",
                "Product complexity increases with new capability — risk of feature bloat diluting core UX",
                "Build timeline uncertainty may lead to scope creep as edge cases emerge during development",
            ],
            conditions=[
                "Conduct user research sprint (20+ interviews) to validate demand before full commitment",
                "Define MVP scope that can ship within 6 weeks to test core value proposition",
                "Ensure no more than 2 existing roadmap commitments are delayed beyond one quarter",
                "Achieve minimum 30% adoption rate among beta users within 4 weeks of soft launch",
            ],
            metrics_to_track=[
                "Feature adoption rate — target 40% of active users within 90 days",
                "User activation: percentage completing core workflow within first session",
                "NPS impact — overall product NPS must not decrease more than 2 points",
                "Retention impact: Day-7 and Day-30 retention for users who engage vs. don't",
                "Support ticket volume for new capability — target below 5% of total tickets",
            ],
            references_to=[],
        )
