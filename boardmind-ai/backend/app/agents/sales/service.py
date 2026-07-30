"""Sales Agent service."""

import json
import logging
from typing import Optional

from app.agents.llm_provider import get_provider, BaseLLMProvider, LLMError, LLMNotConfiguredError
from .prompt import SALES_SYSTEM_PROMPT, build_sales_prompt
from .schema import SalesAgentRequest, SalesAgentResponse

logger = logging.getLogger(__name__)


class SalesAgentService:
    """Service for the Sales Agent in Department Workspace mode."""

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: SalesAgentRequest) -> SalesAgentResponse:
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_sales_prompt(request.scenario, request.context)

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="sales",
            llm_generate=self.llm.generate,
            system_prompt=SALES_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> SalesAgentResponse:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        data = json.loads(cleaned)
        data["agent_id"] = "sales"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return SalesAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: SalesAgentRequest) -> SalesAgentResponse:
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "sales")

        if any(w in scenario_lower for w in ["delay", "cut", "reduce", "remove"]):
            position = "oppose"
            confidence = 0.8
            pipeline_impact = "disruption"
            competitive_effect = "disadvantage"
        elif any(w in scenario_lower for w in ["launch", "expand", "partner", "price increase"]):
            position = "support"
            confidence = 0.75
            pipeline_impact = "new pipeline"
            competitive_effect = "advantage"
        elif any(w in scenario_lower for w in ["invest", "hire", "build"]):
            position = "conditional"
            confidence = 0.6
            pipeline_impact = "acceleration"
            competitive_effect = "advantage"
        else:
            position = "neutral"
            confidence = 0.5
            pipeline_impact = "new pipeline"
            competitive_effect = "neutral"

        return SalesAgentResponse(
            agent_id="sales",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "revenue_upside": (
                    "Estimated $800K-$2M additional ARR opportunity within 12 months, "
                    "depending on execution speed and market reception. Target: 15-30 "
                    "net-new deals at current average deal size."
                ),
                "revenue_risk": (
                    "Potential revenue at risk: $300-600K from pipeline disruption or "
                    "customer confusion during transition. Existing committed deals "
                    "must be protected."
                ),
                "pipeline_impact": pipeline_impact,
                "deal_cycle_effect": "unchanged",
                "competitive_effect": competitive_effect,
            },
            summary=(
                f"From a CRO perspective, this proposal is {position} — the revenue "
                f"opportunity is real but execution timing and customer impact need "
                f"careful management."
            ),
            rationale=(
                evidence_prefix +
                "From a pure revenue standpoint, this proposal opens a meaningful pipeline "
                "opportunity. The addressable accounts are identifiable and our existing "
                "relationships give us credibility to have these conversations. The key "
                "question is speed-to-revenue: how quickly can we convert interest into "
                "closed deals?\n\n"
                "Our sales team's capacity is a consideration. Taking on new responsibilities "
                "without adequate enablement or headcount risks spreading the team thin "
                "and impacting existing deal velocity. I need confidence that we can execute "
                "without sacrificing current pipeline commitments.\n\n"
                "Customer relationships are the foundation here. Any change that confuses "
                "existing accounts or creates trust concerns must be handled with proactive "
                "communication. Our best customers should hear about changes from us first, "
                "not discover them in market."
            ),
            risks=[
                "Pipeline disruption if sales team is pulled into new initiative without adequate capacity planning",
                "Customer trust erosion if existing accounts perceive they are deprioritized for new opportunity",
                "Competitive vulnerability: while we retool, competitors advance on accounts we're distracted from",
                "Deal cycle extension if buyer confusion requires additional education and re-qualification",
            ],
            conditions=[
                "Protect all deals currently in pipeline — no pricing or scope changes for committed prospects",
                "Provide sales enablement materials and training before market-facing launch",
                "Confirm operations can deliver on timeline commitments before we make customer promises",
                "Establish clear quota credit and compensation rules for new business before team is asked to sell",
            ],
            customer_impact=(
                "Key accounts will need proactive outreach to manage expectations and "
                "demonstrate continued commitment. Strategic customers should receive "
                "executive communication. New prospects entering pipeline will benefit "
                "from clearer value proposition. Overall relationship impact is manageable "
                "if communication is prioritized."
            ),
            references_to=[],
        )
