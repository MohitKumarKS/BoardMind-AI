"""HR Agent service."""

import json
import logging
from typing import Optional

from app.agents.llm_provider import get_provider, BaseLLMProvider, LLMError, LLMNotConfiguredError
from .prompt import HR_SYSTEM_PROMPT, build_hr_prompt
from .schema import HRAgentRequest, HRAgentResponse

logger = logging.getLogger(__name__)


class HRAgentService:
    """Service for the HR Agent in Department Workspace mode."""

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: HRAgentRequest) -> HRAgentResponse:
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_hr_prompt(request.scenario, request.context)
        raw_response = await self.llm.generate(HR_SYSTEM_PROMPT, user_prompt)
        return self._parse_and_validate(raw_response)

    def _parse_and_validate(self, raw_response: str) -> HRAgentResponse:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        data = json.loads(cleaned)
        data["agent_id"] = "hr"
        data["round"] = 1
        data["references_to"] = []
        return HRAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: HRAgentRequest) -> HRAgentResponse:
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "hr")

        if any(w in scenario_lower for w in ["layoff", "reduction", "cut staff", "fire"]):
            position = "oppose"
            confidence = 0.85
            headcount = "reduction"
            culture_impact = "negative"
            change_complexity = "high"
        elif any(w in scenario_lower for w in ["hire", "recruit", "grow team", "expand team"]):
            position = "support"
            confidence = 0.7
            headcount = "hiring"
            culture_impact = "positive"
            change_complexity = "medium"
        elif any(w in scenario_lower for w in ["restructure", "reorganize", "merge"]):
            position = "conditional"
            confidence = 0.6
            headcount = "redeployment"
            culture_impact = "negative"
            change_complexity = "high"
        else:
            position = "conditional"
            confidence = 0.6
            headcount = "none"
            culture_impact = "neutral"
            change_complexity = "medium"

        if any(w in scenario_lower for w in ["ai", "automation", "technical", "engineering"]):
            skill_gap = "significant"
        elif any(w in scenario_lower for w in ["new", "different", "expand"]):
            skill_gap = "minor"
        else:
            skill_gap = "none"

        return HRAgentResponse(
            agent_id="hr",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "headcount_change": headcount,
                "skill_gap": skill_gap,
                "culture_impact": culture_impact,
                "change_complexity": change_complexity,
                "timeline_to_readiness": (
                    "3-6 months for full organizational readiness including hiring, "
                    "onboarding, training, and cultural integration"
                ),
            },
            summary=(
                f"From a CHRO perspective, this proposal requires {change_complexity} "
                f"change management investment and careful attention to people impact."
            ),
            rationale=(
                evidence_prefix +
                "Every organizational change has a human cost. The people who will be "
                "most affected by this decision deserve transparent communication, "
                "adequate preparation time, and genuine support through the transition. "
                "My primary concern is whether we are setting our teams up for success "
                "or asking them to absorb more change than they can sustainably handle.\n\n"
                "The talent implications need careful consideration. If this requires new "
                "skills or capabilities, we must be honest about the timeline for hiring, "
                "onboarding, and integration. Rushed hiring leads to culture dilution and "
                "poor retention. If we need existing team members to take on new "
                "responsibilities, we must assess their capacity honestly — not just "
                "whether they technically could, but whether it's fair to ask.\n\n"
                "I recommend a phased approach with explicit people readiness gates. "
                "Before each phase advances, we should confirm: (1) teams have been "
                "communicated to transparently, (2) necessary skills are in place or "
                "actively being developed, (3) workload remains sustainable, and "
                "(4) engagement metrics have not deteriorated."
            ),
            risks=[
                "Team burnout risk if implementation timeline doesn't account for learning curves and adjustment periods",
                "Culture erosion if speed of change outpaces the organization's ability to adapt and maintain values",
                "Talent retention risk: high-performers may leave if they feel change is poorly managed or unfair",
                "Knowledge loss if experienced team members are moved to new roles without adequate transition planning",
            ],
            conditions=[
                "Conduct employee impact assessment before finalizing implementation timeline",
                "Develop communication plan that gives affected teams advance notice and input opportunity",
                "Ensure managers receive change leadership training before cascading to their teams",
                "Establish workload monitoring with explicit escalation path if teams report unsustainable demands",
            ],
            change_management_needs=[
                "Executive communication to all affected teams explaining the 'why' before the 'what'",
                "Manager enablement sessions providing talking points and FAQ for team conversations",
                "Skills assessment for impacted roles with development plans for gaps identified",
                "Feedback mechanism (anonymous pulse surveys) to monitor morale during transition",
                "Celebration milestones to recognize teams navigating the change successfully",
            ],
            references_to=[],
        )
