"""Chief Risk Officer Agent service.

This module provides the RiskAgentService which:
1. Receives a business proposal
2. Builds the Risk prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a RiskAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import RISK_SYSTEM_PROMPT, build_risk_prompt
from .schema import RiskAgentRequest, RiskAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class RiskAgentService:
    """Service for the Risk Agent in Department Workspace mode.

    Usage:
        service = RiskAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: RiskAgentRequest) -> RiskAgentResponse:
        """Analyze a business proposal from the CRO perspective."""
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_risk_prompt(request.scenario, request.context)
        logger.info("Invoking LLM for Risk Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="risk",
            llm_generate=self.llm.generate,
            system_prompt=RISK_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> RiskAgentResponse:
        """Parse raw LLM output and validate against the schema."""
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM response is not valid JSON: {e}")

        data["agent_id"] = "risk"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return RiskAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: RiskAgentRequest) -> RiskAgentResponse:
        """Generate a realistic mock response for development and testing."""
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "risk")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["low risk", "proven", "incremental", "tested", "validated"]):
            position = "support"
            confidence = 0.75
        elif any(word in scenario_lower for word in ["unprecedented", "bet the company", "all-in", "unproven market"]):
            position = "oppose"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["expand", "invest", "launch", "acquire", "new market"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine risk level
        if any(word in scenario_lower for word in ["bet the company", "all revenue", "existential", "regulatory penalty"]):
            risk_level = "critical"
        elif any(word in scenario_lower for word in ["international", "acquisition", "major", "restructure"]):
            risk_level = "high"
        elif any(word in scenario_lower for word in ["pilot", "small", "test", "limited"]):
            risk_level = "low"
        else:
            risk_level = "medium"

        return RiskAgentResponse(
            agent_id="risk",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "risk_exposure": (
                    "Estimated maximum loss exposure: $1.5M-$4M (95th percentile) "
                    "depending on scenario materialization. Expected loss (probability-"
                    "weighted): $600K-$1.2M. Value at Risk (1-year, 95% CI): $2.8M. "
                    "This represents 8-15% of annual operating budget."
                ),
                "probability_assessment": (
                    "Probability of material adverse outcome: 25-35% based on "
                    "comparable historical initiatives and market conditions. "
                    "Key risk drivers: execution complexity (40% contribution), "
                    "market uncertainty (35%), and resource constraints (25%). "
                    "Monte Carlo simulation suggests 30% probability of >$1M loss."
                ),
                "mitigation_strategy": (
                    "Recommended mitigations: (1) Phased implementation with stage "
                    "gates reduces max exposure by 60% ($4M → $1.6M). (2) Risk "
                    "transfer via insurance covers catastrophic scenarios ($200K premium "
                    "for $2M coverage). (3) Hedging through diversified approach reduces "
                    "concentration risk. Combined mitigation effectiveness: 65-75%."
                ),
                "residual_risk": (
                    "Post-mitigation residual risk: $400K-$900K expected loss "
                    "(within board-approved risk appetite of $1M per initiative). "
                    "Residual probability of material loss: 10-15%. Acceptable "
                    "if monitoring framework is in place for early warning."
                ),
                "risk_level": risk_level,
            },
            summary=(
                f"From a risk management perspective, this proposal is {position} — "
                f"the risk exposure {'is within organizational appetite after mitigation' if position in ('support', 'conditional') else 'requires further analysis to determine acceptability'} "
                f"with {confidence:.0%} confidence in this assessment."
            ),
            rationale=(
                evidence_prefix +
                "From an enterprise risk perspective, this proposal introduces "
                "quantifiable risk that must be assessed against our organizational "
                "risk appetite. Using probability-weighted scenario analysis, the "
                "expected loss ranges from $600K-$1.2M, with tail risk (95th "
                "percentile) reaching $4M in worst-case scenarios.\n\n"
                "The primary risk drivers are execution complexity and market "
                "uncertainty. Historical analogs for similar initiatives show a "
                "25-35% failure rate when attempted without phased implementation. "
                "However, organizations that employed stage-gate approaches reduced "
                "their failure rate to 10-15% — a significant risk reduction that "
                "brings exposure within acceptable tolerances.\n\n"
                "My recommendation is to proceed with a structured risk mitigation "
                "framework: phased implementation with defined kill criteria at each "
                "gate, risk transfer for catastrophic scenarios, and continuous "
                "monitoring with early warning indicators. With these controls in "
                "place, residual risk falls within our board-approved risk appetite."
            ),
            risks=[
                "Execution risk — 25-35% probability of significant timeline overrun or scope failure based on historical analogs",
                "Concentration risk — single initiative consuming disproportionate share of risk budget limits capacity for other opportunities",
                "Correlation risk — adverse outcome may coincide with market downturn, amplifying impact beyond standalone assessment",
                "Reputation risk — public failure could damage brand value by estimated $2-5M in market cap impact",
            ],
            conditions=[
                "Implement phased approach with defined risk thresholds at each stage gate",
                "Establish early warning indicators with automated monitoring and escalation protocols",
                "Secure risk transfer mechanism (insurance or hedging) for tail-risk scenarios exceeding $2M",
                "Board-level risk appetite confirmation for this specific initiative before proceeding",
            ],
            metrics_to_track=[
                "Risk exposure vs. approved risk appetite — flag when exceeding 80% of limit",
                "Key Risk Indicator (KRI) dashboard — update weekly with trend analysis",
                "Loss event frequency and severity — compare to baseline and projections",
                "Risk mitigation effectiveness — measure actual vs. estimated risk reduction",
                "Scenario probability updates — Bayesian refresh as new information emerges",
            ],
            references_to=[],
        )
