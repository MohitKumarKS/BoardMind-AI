"""IT Agent service."""

import json
import logging
from typing import Optional

from app.agents.llm_provider import get_provider, BaseLLMProvider, LLMError, LLMNotConfiguredError
from .prompt import IT_SYSTEM_PROMPT, build_it_prompt
from .schema import ITAgentRequest, ITAgentResponse

logger = logging.getLogger(__name__)


class ITAgentService:
    """Service for the IT Agent in Department Workspace mode."""

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: ITAgentRequest) -> ITAgentResponse:
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_it_prompt(request.scenario, request.context)

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="it",
            llm_generate=self.llm.generate,
            system_prompt=IT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> ITAgentResponse:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        data = json.loads(cleaned)
        data["agent_id"] = "it"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return ITAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: ITAgentRequest) -> ITAgentResponse:
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "it")

        if any(w in scenario_lower for w in ["simple", "existing", "minor", "standard"]):
            feasibility = "straightforward"
            security_risk = "low"
            infra_needs = "existing"
            integration = "low"
            debt_impact = "neutral"
            position = "support"
            confidence = 0.85
        elif any(w in scenario_lower for w in ["migrate", "overhaul", "replace", "rebuild"]):
            feasibility = "complex"
            security_risk = "medium"
            infra_needs = "significant_investment"
            integration = "high"
            debt_impact = "reduces"
            position = "conditional"
            confidence = 0.6
        elif any(w in scenario_lower for w in ["ai", "ml", "machine learning", "blockchain"]):
            feasibility = "moderate"
            security_risk = "medium"
            infra_needs = "significant_investment"
            integration = "medium"
            debt_impact = "neutral"
            position = "conditional"
            confidence = 0.65
        else:
            feasibility = "moderate"
            security_risk = "medium"
            infra_needs = "minor_additions"
            integration = "medium"
            debt_impact = "neutral"
            position = "conditional"
            confidence = 0.6

        return ITAgentResponse(
            agent_id="it",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "feasibility": feasibility,
                "security_risk": security_risk,
                "infrastructure_needs": infra_needs,
                "integration_complexity": integration,
                "technical_debt_impact": debt_impact,
            },
            summary=(
                f"From a CTO perspective, this is technically {feasibility} — "
                f"achievable with proper planning and the right architectural approach."
            ),
            rationale=(
                evidence_prefix +
                "Technically, this proposal is within our capability to deliver, though "
                "the implementation path requires careful architecture decisions that will "
                "affect long-term maintainability. The core feasibility question is not "
                "'can we build this?' but 'can we build this in a way that doesn't create "
                "compounding technical debt?'\n\n"
                "From a security standpoint, any new system surface increases our attack "
                "vector. The proposal involves data flows and system integrations that "
                "require security review before implementation begins. I recommend a "
                "threat modeling exercise to identify specific vulnerabilities and design "
                "mitigations into the architecture from day one rather than bolting them "
                "on later.\n\n"
                "Infrastructure considerations are manageable. Our current platform can "
                "accommodate the initial implementation, though scaling beyond pilot may "
                "require additional investment. I recommend validating performance "
                "assumptions with a proof-of-concept before committing to the full build. "
                "Integration with existing systems is the primary complexity driver — each "
                "touchpoint adds risk and testing surface area."
            ),
            risks=[
                "Integration complexity with existing systems may exceed initial estimates — each API touchpoint adds testing and maintenance burden",
                "Security surface expansion without adequate threat modeling creates vulnerability window during and after deployment",
                "Technical debt accumulation if implementation is rushed to meet aggressive timelines without architecture review",
                "Platform scalability uncertainty: current infrastructure handles pilot load but production scale is unvalidated",
            ],
            conditions=[
                "Conduct architecture review and threat modeling before development begins",
                "Validate integration assumptions with proof-of-concept for highest-risk system touchpoints",
                "Allocate 20% of development time for security hardening and testing",
                "Establish performance benchmarks and load testing criteria before production launch",
            ],
            effort_estimate=(
                "Estimated effort: 3-5 months for a team of 2-4 engineers. "
                "Phase 1 (architecture + PoC): 3-4 weeks. "
                "Phase 2 (core implementation): 6-10 weeks. "
                "Phase 3 (integration + security): 4-6 weeks. "
                "Range accounts for integration complexity uncertainty and assumes "
                "no major architectural pivots are required."
            ),
            references_to=[],
        )
