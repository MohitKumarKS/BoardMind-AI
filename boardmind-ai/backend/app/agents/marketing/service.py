"""Marketing Agent service."""

import json
import logging
from typing import Optional

from app.agents.llm_provider import get_provider, BaseLLMProvider, LLMError, LLMNotConfiguredError
from .prompt import MARKETING_SYSTEM_PROMPT, build_marketing_prompt
from .schema import MarketingAgentRequest, MarketingAgentResponse

logger = logging.getLogger(__name__)


class MarketingAgentService:
    """Service for the Marketing Agent in Department Workspace mode."""

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: MarketingAgentRequest) -> MarketingAgentResponse:
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_marketing_prompt(request.scenario, request.context)

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="marketing",
            llm_generate=self.llm.generate,
            system_prompt=MARKETING_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> MarketingAgentResponse:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        data = json.loads(cleaned)
        data["agent_id"] = "marketing"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return MarketingAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: MarketingAgentRequest) -> MarketingAgentResponse:
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "marketing")

        if any(w in scenario_lower for w in ["rebrand", "brand", "positioning"]):
            position = "conditional"
            confidence = 0.7
            brand_impact = "positive"
        elif any(w in scenario_lower for w in ["cut", "reduce", "eliminate"]):
            position = "oppose"
            confidence = 0.7
            brand_impact = "negative"
        elif any(w in scenario_lower for w in ["launch", "expand", "partner"]):
            position = "support"
            confidence = 0.7
            brand_impact = "positive"
        else:
            position = "neutral"
            confidence = 0.5
            brand_impact = "neutral"

        if any(w in scenario_lower for w in ["international", "europe", "global"]):
            complexity = "high"
        elif any(w in scenario_lower for w in ["pilot", "test", "small"]):
            complexity = "low"
        else:
            complexity = "medium"

        return MarketingAgentResponse(
            agent_id="marketing",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "market_opportunity": (
                    "Based on the proposal scope, the addressable market opportunity "
                    "is estimated at $500M-$2B depending on segment definition and "
                    "geographic focus. Achievable share within 12-18 months: 0.5-2%."
                ),
                "brand_impact": brand_impact,
                "competitive_position": "strengthened" if position == "support" else "unchanged",
                "customer_segments_affected": [
                    "Primary: existing customer base seeking expanded value",
                    "Secondary: net-new prospects in adjacent segments",
                ],
                "go_to_market_complexity": complexity,
            },
            summary=(
                f"From a CMO perspective, this proposal presents a {complexity}-complexity "
                f"market opportunity that requires careful positioning to maximize brand impact."
            ),
            rationale=(
                evidence_prefix +
                "From a market positioning standpoint, this proposal touches several "
                "critical brand and competitive dimensions. The addressable audience is "
                "meaningful, and there is clear demand signal in the market for solutions "
                "in this space.\n\n"
                "However, the competitive landscape is not empty. Incumbents have established "
                "positioning, and late entry requires a differentiated narrative that gives "
                "buyers a compelling reason to consider us. Our existing brand equity provides "
                "a foundation, but we must be intentional about how we extend it into this "
                "new context without dilution.\n\n"
                "The go-to-market approach should prioritize audience validation before "
                "broad spend. I recommend a focused launch strategy targeting our highest-"
                "propensity segments with messaging tested through lightweight channels "
                "before committing to full-funnel investment."
            ),
            risks=[
                "Brand perception risk if positioning is unclear — existing customers may be confused by mixed messaging",
                "Competitive response: established players will counter-position aggressively on awareness and trust",
                "Channel misalignment: current marketing infrastructure may not suit the new audience's discovery patterns",
                "Timing risk: market window may be narrower than assumed if competitor momentum continues",
            ],
            conditions=[
                "Conduct positioning research with 15-20 target buyers before committing to messaging",
                "Allocate dedicated marketing budget separate from existing programs",
                "Develop clear brand architecture that defines how this offering relates to our core identity",
                "Establish awareness and consideration benchmarks within first 90 days as go/no-go gate",
            ],
            recommended_actions=[
                "Commission competitive positioning audit to identify differentiation white space",
                "Develop and test 3 messaging variants with target audience before launch",
                "Build dedicated landing experience and content strategy for the new audience segment",
                "Plan phased channel activation: organic/content first, paid amplification after validation",
            ],
            references_to=[],
        )
