"""ESG & Sustainability Officer service.

This module provides the ESGAgentService which:
1. Receives a business proposal
2. Builds the ESG prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns an ESGAgentResponse object
"""

import json
import os
import logging
from typing import Optional

from .prompt import ESG_SYSTEM_PROMPT, build_esg_prompt
from .schema import ESGAgentRequest, ESGAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


# Backward-compatible alias
LLMProvider = get_provider


class ESGAgentService:
    """Service for the ESG & Sustainability Officer in Department Workspace mode.

    This class encapsulates the complete ESG Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = ESGAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: ESGAgentRequest) -> ESGAgentResponse:
        """Analyze a business proposal from the ESG perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated ESGAgentResponse with complete ESG analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_esg_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for ESG Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="esg",
            llm_generate=self.llm.generate,
            system_prompt=ESG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> ESGAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated ESGAgentResponse.

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
        data["agent_id"] = "esg"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return ESGAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: ESGAgentRequest) -> ESGAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "esg")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["renewable", "green", "sustainable", "reduce emissions", "solar"]):
            position = "support"
            confidence = 0.85
        elif any(word in scenario_lower for word in ["fossil", "pollut", "deforest", "coal", "dump"]):
            position = "oppose"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["expand", "grow", "new facility", "manufacturing"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine ESG risk level
        if any(word in scenario_lower for word in ["toxic", "hazardous", "critical", "violation"]):
            esg_risk = "critical"
        elif any(word in scenario_lower for word in ["significant", "large-scale", "international", "heavy"]):
            esg_risk = "high"
        elif any(word in scenario_lower for word in ["pilot", "small", "test", "limited"]):
            esg_risk = "low"
        else:
            esg_risk = "medium"

        return ESGAgentResponse(
            agent_id="esg",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "environmental_impact": (
                    "Estimated carbon footprint increase of 800-1,200 tonnes CO2e annually "
                    "from expanded operations. Energy consumption projected at 2.4 GWh/year. "
                    "Waste generation expected to rise 15-25% without mitigation measures. "
                    "Water usage impact requires assessment against local watershed capacity."
                ),
                "social_impact": (
                    "Community stakeholder engagement required for local operations. "
                    "Workforce diversity metrics must be maintained or improved — current "
                    "baseline shows 28% underrepresented groups. Labor practice compliance "
                    "across supply chain requires audit. Positive job creation potential of "
                    "50-100 roles in local community."
                ),
                "governance_implications": (
                    "Board-level ESG committee oversight required for initiatives of this "
                    "scale. Quarterly sustainability reporting cadence must be established. "
                    "Executive compensation ESG linkage should be reviewed. Whistleblower "
                    "and ethics reporting channels must extend to new operations."
                ),
                "sustainability_score": (
                    "Partial alignment with GRI 305 (Emissions) and GRI 302 (Energy). "
                    "TCFD climate risk disclosure gaps identified in transition risk assessment. "
                    "SASB materiality mapping required for sector-specific standards. "
                    "UN SDG alignment: potential positive contribution to SDGs 8, 9, 12."
                ),
                "esg_risk": esg_risk,
            },
            summary=(
                f"From an ESG perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — sustainability alignment requires "
                f"verified environmental mitigation and governance oversight."
            ),
            rationale=(
                evidence_prefix +
                "From a sustainability perspective, this proposal presents both "
                "opportunities and challenges across the ESG spectrum. The environmental "
                "dimension requires careful management — any operational expansion carries "
                "inherent carbon and resource implications that must be quantified and "
                "mitigated to align with our stated climate commitments.\n\n"
                "On the social dimension, the proposal has potential positive impacts "
                "through job creation and community development, but these must be "
                "balanced against supply chain labor practice risks and diversity "
                "commitments. Our stakeholder engagement framework requires proactive "
                "community consultation before operational changes of this magnitude.\n\n"
                "From a governance standpoint, this initiative requires board-level "
                "ESG oversight and integration into our existing sustainability reporting "
                "framework. The TCFD-aligned climate risk assessment must be completed "
                "before proceeding. I recommend establishing clear ESG KPIs with "
                "executive accountability to ensure sustainability objectives are not "
                "subordinated to short-term operational goals."
            ),
            risks=[
                "Carbon emissions increase may exceed Science Based Targets initiative (SBTi) pathway — risking net-zero commitment timeline",
                "Greenwashing exposure if sustainability claims are not backed by verified third-party data and audits",
                "Supply chain ESG risks in new operations may not be visible without comprehensive Scope 3 assessment",
                "Reputational risk from stakeholder and community opposition if environmental impact is not proactively managed",
            ],
            conditions=[
                "Complete Scope 1, 2, and 3 greenhouse gas inventory for proposed operations before approval",
                "Establish carbon offset or reduction plan to maintain net-zero trajectory alignment",
                "Conduct community stakeholder engagement and social impact assessment",
                "Integrate ESG metrics into project governance with quarterly board reporting",
            ],
            metrics_to_track=[
                "Total greenhouse gas emissions (Scope 1, 2, 3) in tonnes CO2e — quarterly measurement",
                "ESG rating impact — monitor MSCI, Sustainalytics, and CDP scores",
                "Community engagement satisfaction score — baseline and quarterly surveys",
                "Diversity and inclusion metrics across new operations — target parity with company baseline",
                "Water usage intensity and waste diversion rate — monthly tracking",
            ],
            references_to=[],
        )
