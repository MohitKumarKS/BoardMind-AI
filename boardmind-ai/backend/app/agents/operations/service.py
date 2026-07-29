"""Operations Agent service."""

import json
import logging
from typing import Optional

from app.agents.llm_provider import get_provider, BaseLLMProvider, LLMError, LLMNotConfiguredError
from .prompt import OPERATIONS_SYSTEM_PROMPT, build_operations_prompt
from .schema import OperationsAgentRequest, OperationsAgentResponse

logger = logging.getLogger(__name__)


class OperationsAgentService:
    """Service for the Operations Agent in Department Workspace mode."""

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: OperationsAgentRequest) -> OperationsAgentResponse:
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_operations_prompt(request.scenario, request.context)
        raw_response = await self.llm.generate(OPERATIONS_SYSTEM_PROMPT, user_prompt)
        return self._parse_and_validate(raw_response)

    def _parse_and_validate(self, raw_response: str) -> OperationsAgentResponse:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        data = json.loads(cleaned)
        data["agent_id"] = "operations"
        data["round"] = 1
        data["references_to"] = []
        return OperationsAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: OperationsAgentRequest) -> OperationsAgentResponse:
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "operations")

        if any(w in scenario_lower for w in ["simple", "small", "minor", "optimize"]):
            position = "support"
            confidence = 0.8
            complexity = "low"
            capacity = "within capacity"
        elif any(w in scenario_lower for w in ["international", "transform", "overhaul", "migrate"]):
            position = "conditional"
            confidence = 0.55
            complexity = "high"
            capacity = "overload"
        elif any(w in scenario_lower for w in ["expand", "launch", "build", "hire"]):
            position = "conditional"
            confidence = 0.65
            complexity = "medium"
            capacity = "stretch"
        else:
            position = "neutral"
            confidence = 0.5
            complexity = "medium"
            capacity = "stretch"

        return OperationsAgentResponse(
            agent_id="operations",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "execution_complexity": complexity,
                "timeline_estimate": (
                    "Realistic timeline: 4-8 months end-to-end. Phase 1 (foundation): "
                    "6-8 weeks. Phase 2 (core delivery): 8-12 weeks. Phase 3 (stabilization): "
                    "4-6 weeks. Add 2-4 weeks buffer for dependencies."
                ),
                "resource_requirements": (
                    "Requires 2-3 dedicated team members for core execution, "
                    "cross-functional support from 2-3 other teams on a part-time basis, "
                    "and potentially 1-2 external vendors for specialized capabilities."
                ),
                "capacity_impact": capacity,
                "dependencies": [
                    "Technical infrastructure readiness (coordinate with IT)",
                    "Headcount availability (coordinate with HR on hiring timeline)",
                    "Budget approval and vendor procurement (Finance sign-off required)",
                ],
            },
            summary=(
                f"From a COO perspective, this is a {complexity}-complexity initiative "
                f"that is executable with proper phasing and resource commitment."
            ),
            rationale=(
                evidence_prefix +
                "Operationally, this initiative is feasible but not trivial. The execution "
                "path has several dependencies that must be resolved sequentially — they "
                "cannot be parallelized without risk. The critical path runs through "
                "resource availability, technical readiness, and process design. Any "
                "slip in these areas cascades to the overall timeline.\n\n"
                "Current operational capacity is already committed to existing priorities. "
                "Taking this on requires either deprioritizing something else, adding "
                "headcount (which has its own 6-8 week ramp-up time), or accepting "
                "quality trade-offs on current deliverables. I do not recommend the "
                "third option.\n\n"
                "The phased approach I recommend allows us to validate execution "
                "assumptions at each stage before committing further resources. "
                "Each phase has a clear deliverable and readiness gate. If Phase 1 "
                "reveals unforeseen complexity, we can adjust scope or timeline "
                "before Phase 2 investment."
            ),
            risks=[
                "Timeline compression risk: if Phase 1 dependencies slip, the entire schedule shifts by the same margin",
                "Resource contention: current team commitments mean new work competes with existing delivery obligations",
                "Quality degradation risk if team is stretched across too many concurrent initiatives",
                "Vendor dependency: external providers have their own timelines and may not align with our urgency",
            ],
            conditions=[
                "Confirm dedicated resource allocation (named individuals, not 'spare capacity') before Phase 1 start",
                "Resolve critical-path dependencies (technical infrastructure, headcount) before committing to Phase 2 timeline",
                "Establish operational readiness gates between phases with explicit go/no-go criteria",
                "Accept realistic timeline with buffer — compressed timelines create execution debt that surfaces later",
            ],
            implementation_phases=[
                "Phase 1 — Foundation (Weeks 1-8): Secure resources, resolve dependencies, design core processes, establish tooling",
                "Phase 2 — Core Delivery (Weeks 9-20): Execute primary workstreams, validate with early results, adjust approach",
                "Phase 3 — Stabilization (Weeks 21-26): Harden processes, document procedures, train team, transition to steady-state",
                "Phase 4 — Optimization (Ongoing): Monitor operational metrics, identify efficiency gains, iterate on process",
            ],
            references_to=[],
        )
