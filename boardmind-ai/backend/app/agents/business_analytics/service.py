"""Business Analytics Agent service."""

import json
import logging
from typing import Optional

from app.agents.llm_provider import get_provider, BaseLLMProvider
from .prompt import ANALYTICS_SYSTEM_PROMPT, build_analytics_prompt
from .schema import AnalyticsAgentRequest, AnalyticsAgentResponse

logger = logging.getLogger(__name__)


class AnalyticsAgentService:
    """Service for the Business Analytics Agent in Department Workspace mode."""

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: AnalyticsAgentRequest) -> AnalyticsAgentResponse:
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_analytics_prompt(request.scenario, request.context)

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="business_analytics",
            llm_generate=self.llm.generate,
            system_prompt=ANALYTICS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> AnalyticsAgentResponse:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        data = json.loads(cleaned)
        data["agent_id"] = "business_analytics"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return AnalyticsAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: AnalyticsAgentRequest) -> AnalyticsAgentResponse:
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "business_analytics")

        # Assess evidence based on scenario signals
        has_data = any(w in scenario_lower for w in ["data", "metric", "measured", "tracked", "survey"])
        has_numbers = any(w in scenario_lower for w in ["$", "%", "million", "thousand", "revenue"])

        if has_data and has_numbers:
            evidence_strength = "moderate"
            data_availability = "partially_available"
            projection_confidence = "medium"
            position = "conditional"
            confidence = 0.65
        elif has_numbers:
            evidence_strength = "weak"
            data_availability = "partially_available"
            projection_confidence = "low"
            position = "conditional"
            confidence = 0.5
        else:
            evidence_strength = "insufficient"
            data_availability = "not_available"
            projection_confidence = "low"
            position = "neutral"
            confidence = 0.4

        return AnalyticsAgentResponse(
            agent_id="business_analytics",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "evidence_strength": evidence_strength,
                "data_availability": data_availability,
                "projection_confidence": projection_confidence,
                "key_metrics": [
                    "Primary outcome metric aligned to stated goal",
                    "Leading indicators (early signals of success/failure)",
                    "Guardrail metrics (things that must NOT degrade)",
                    "Efficiency metrics (output per unit of input)",
                ],
                "benchmarks": [
                    "Industry median performance for comparable initiatives: typically 60-70% of projected outcomes",
                    "Base rate of success for similar projects in this sector: 35-45%",
                    "Typical timeline variance for this type of initiative: +40-60% over initial estimate",
                ],
            },
            summary=(
                f"The evidence supporting this proposal is {evidence_strength} — "
                f"a structured measurement framework is needed before confident "
                f"decision-making is possible."
            ),
            rationale=(
                evidence_prefix +
                "Examining the evidence basis for this proposal, I find that several key "
                "claims lack sufficient data support to assess with high confidence. The "
                "projections presented may be reasonable, but they rely on assumptions "
                "that have not been validated against actual performance data or relevant "
                "benchmarks. This is not unusual at this stage, but it means we are making "
                "a decision under uncertainty rather than with evidence.\n\n"
                "Industry benchmarks for similar initiatives suggest that actual outcomes "
                "typically achieve 60-70% of initial projections. This is not pessimism — "
                "it is the base rate. Planning for this range rather than best-case "
                "scenarios leads to better resource allocation and more honest progress "
                "assessment.\n\n"
                "What is measurable here? We can define clear success criteria and track "
                "leading indicators from day one. I recommend establishing a measurement "
                "framework before launch that defines: (1) what success looks like "
                "quantitatively, (2) what early signals we should monitor weekly, (3) what "
                "thresholds trigger escalation or pivot, and (4) what data we will collect "
                "to inform future decisions of this type.\n\n"
                "The absence of data should not paralyze decision-making, but it should "
                "inform the approach: smaller initial commitment, faster iteration cycles, "
                "and explicit validation milestones."
            ),
            risks=[
                "Projection confidence is low due to insufficient historical data or validated assumptions",
                "Confirmation bias risk: positive signals may be over-weighted while negative signals are explained away",
                "Measurement gap: if success criteria are not defined upfront, it becomes impossible to objectively evaluate outcomes",
                "Survivorship bias in benchmarks: published success stories may not represent the true base rate of outcomes",
            ],
            conditions=[
                "Define quantitative success criteria before launch — what specific numbers constitute success vs. failure?",
                "Establish weekly leading indicator dashboard visible to all stakeholders from day one",
                "Commit to pre-registered decision thresholds: at what point do we scale up, pivot, or stop?",
                "Collect baseline measurements before intervention begins to enable true before/after comparison",
            ],
            measurement_plan=(
                "Phase 1 (Pre-launch, Week 0): Establish baseline metrics for all key "
                "indicators. Define success = X, acceptable = Y, failure = Z thresholds. "
                "Phase 2 (Weeks 1-4): Monitor leading indicators weekly. Flag any metric "
                "deviating >20% from projected trajectory. "
                "Phase 3 (Week 8): Formal review against pre-defined success criteria. "
                "Data-driven decision: continue, adjust, or stop. "
                "Phase 4 (Week 12): Full outcome assessment with statistical confidence "
                "intervals. Document learnings for future decisions of this type."
            ),
            references_to=[],
        )
