"""Chief Innovation Officer service.

This module provides the InnovationAgentService which:
1. Receives a business proposal
2. Builds the Innovation prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns an InnovationAgentResponse object
"""

import json
import os
import logging
from typing import Optional

from .prompt import INNOVATION_SYSTEM_PROMPT, build_innovation_prompt
from .schema import InnovationAgentRequest, InnovationAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


# Backward-compatible alias
LLMProvider = get_provider


class InnovationAgentService:
    """Service for the Chief Innovation Officer in Department Workspace mode.

    This class encapsulates the complete Innovation Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = InnovationAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: InnovationAgentRequest) -> InnovationAgentResponse:
        """Analyze a business proposal from the innovation perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated InnovationAgentResponse with complete innovation analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_innovation_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for Innovation Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="innovation",
            llm_generate=self.llm.generate,
            system_prompt=INNOVATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> InnovationAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated InnovationAgentResponse.

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
        data["agent_id"] = "innovation"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return InnovationAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: InnovationAgentRequest) -> InnovationAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "innovation")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["breakthrough", "novel", "first-mover", "patent", "disruptive"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["commodity", "mature", "outdated", "incremental", "me-too"]):
            position = "oppose"
            confidence = 0.75
        elif any(word in scenario_lower for word in ["research", "emerging", "prototype", "experiment", "explore"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine innovation risk level
        if any(word in scenario_lower for word in ["unproven", "theoretical", "quantum", "10 year"]):
            innovation_risk = "high"
        elif any(word in scenario_lower for word in ["proven", "established", "standard", "known"]):
            innovation_risk = "low"
        else:
            innovation_risk = "medium"

        return InnovationAgentResponse(
            agent_id="innovation",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "innovation_potential": (
                    "Moderate-to-high innovation potential identified. The proposal combines "
                    "existing technologies in a novel application context that has limited "
                    "market precedent. Differentiation opportunity exists if execution achieves "
                    "technical milestones ahead of emerging competitors. The innovation sits "
                    "at the intersection of Horizon 2 (adjacent innovation) and Horizon 3 "
                    "(transformational), warranting structured exploration."
                ),
                "technology_readiness": (
                    "Current Technology Readiness Level assessed at TRL 3-4 (experimental "
                    "proof of concept validated in laboratory). Advancement to TRL 6 "
                    "(system/subsystem model demonstrated in relevant environment) requires "
                    "12-18 months of focused R&D. Key technical uncertainties center on "
                    "scalability and integration with production systems. Similar approaches "
                    "have reached TRL 5 in academic settings."
                ),
                "research_requirements": (
                    "Estimated R&D investment of $1.5-2.5M over 18 months. Team requirements: "
                    "3-4 senior researchers/engineers with domain expertise, access to "
                    "specialized compute infrastructure, and 1-2 university research "
                    "partnerships for foundational work. Phased approach recommended: "
                    "$500K Phase 1 (6 months) for feasibility, $1-2M Phase 2 (12 months) "
                    "for prototype development."
                ),
                "ip_opportunity": (
                    "Patent landscape analysis indicates 2-4 patentable innovations in "
                    "the proposed approach. Freedom-to-operate review identifies moderate "
                    "white space with 3 relevant prior art clusters. Defensive patent "
                    "strategy recommended alongside offensive filings. Trade secret "
                    "protection viable for proprietary algorithms and training methodologies."
                ),
                "innovation_risk": innovation_risk,
            },
            summary=(
                f"From an innovation perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — the technology shows promising novelty "
                f"but requires structured R&D validation before scaling commitment."
            ),
            rationale=(
                evidence_prefix +
                "From an innovation strategy perspective, this proposal represents a "
                "meaningful opportunity to build differentiated capabilities. The "
                "technology approach combines established components in a novel "
                "configuration that, if validated, could create sustainable competitive "
                "advantage. The key question is whether the technical uncertainties "
                "can be resolved within an acceptable timeframe and budget.\n\n"
                "The Technology Readiness Level assessment places this at TRL 3-4, "
                "meaning the fundamental principles are proven but significant "
                "engineering work remains to reach production readiness. This is "
                "typical for Horizon 2-3 innovations and is not disqualifying, but "
                "it does require a staged investment approach with clear go/no-go "
                "gates. The research talent requirements are achievable but competitive "
                "in the current market.\n\n"
                "From an IP perspective, the patent landscape offers meaningful "
                "filing opportunities. Early defensive filings are recommended to "
                "establish priority dates while the full R&D program develops. The "
                "innovation portfolio balance benefits from this addition — our "
                "current portfolio is weighted toward Horizon 1 (core) with "
                "insufficient investment in transformational opportunities. This "
                "proposal helps rebalance toward a healthier 70/20/10 allocation."
            ),
            risks=[
                "Technology maturation timeline may exceed projections — TRL advancement from 3 to 6 has high historical variance (12-36 months)",
                "Key research talent acquisition competitive risk — specialized researchers in this domain are scarce and highly sought",
                "Prior art collision risk — 3 identified patent clusters may narrow freedom-to-operate if competitors file first",
                "Integration complexity with existing production systems may require architectural changes not scoped in initial R&D plan",
            ],
            conditions=[
                "Establish Phase 1 feasibility milestone: demonstrate TRL 4 advancement within 6 months with $500K budget cap",
                "Secure at least 2 senior researchers with relevant domain expertise before committing Phase 2 funding",
                "Complete freedom-to-operate patent analysis and file provisional applications for identified innovations",
                "Define quantitative success criteria for Phase 1 to Phase 2 gate decision with independent technical review",
            ],
            metrics_to_track=[
                "Technology Readiness Level advancement — target TRL 6 within 18 months",
                "Patent applications filed and granted — target 2-4 provisional filings in Year 1",
                "R&D milestone completion rate — percentage of planned milestones achieved on schedule",
                "Innovation pipeline value — projected market opportunity of validated innovations",
                "Research partnership productivity — publications, shared IP, and technology transfer metrics",
            ],
            references_to=[],
        )
