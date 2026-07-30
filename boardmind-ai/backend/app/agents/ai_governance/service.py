"""AI Governance & Ethics Officer service.

This module provides the AIGovernanceAgentService which:
1. Receives a business proposal
2. Builds the AI Governance prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns an AIGovernanceAgentResponse object
"""

import json
import os
import logging
from typing import Optional

from .prompt import AI_GOVERNANCE_SYSTEM_PROMPT, build_ai_governance_prompt
from .schema import AIGovernanceAgentRequest, AIGovernanceAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


# Backward-compatible alias
LLMProvider = get_provider


class AIGovernanceAgentService:
    """Service for the AI Governance & Ethics Officer in Department Workspace mode.

    This class encapsulates the complete AI Governance Agent workflow:
    prompt construction, LLM invocation, response validation, and
    structured output delivery.

    Usage:
        service = AIGovernanceAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: AIGovernanceAgentRequest) -> AIGovernanceAgentResponse:
        """Analyze a business proposal from the AI governance perspective.

        Args:
            request: The business scenario to analyze.

        Returns:
            Validated AIGovernanceAgentResponse with complete AI ethics analysis.

        Raises:
            LLMNotConfiguredError: When no LLM is available and mock is not requested.
            LLMError: When the LLM invocation fails.
            ValidationError: When the LLM response doesn't match the schema.
        """
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_ai_governance_prompt(request.scenario, request.context)

        logger.info("Invoking LLM for AI Governance Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="ai_governance",
            llm_generate=self.llm.generate,
            system_prompt=AI_GOVERNANCE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> AIGovernanceAgentResponse:
        """Parse raw LLM output and validate against the schema.

        Args:
            raw_response: Raw JSON string from the LLM.

        Returns:
            Validated AIGovernanceAgentResponse.

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
        data["agent_id"] = "ai_governance"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return AIGovernanceAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: AIGovernanceAgentRequest) -> AIGovernanceAgentResponse:
        """Generate a realistic mock response for development and testing.

        This mock demonstrates the expected output quality and structure
        without requiring an LLM. It analyzes keywords in the scenario
        to produce a contextually relevant response.
        """
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "ai_governance")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["transparent", "explainable", "audited", "fair", "human-in-the-loop"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["autonomous", "no oversight", "black box", "unregulated", "discriminat"]):
            position = "oppose"
            confidence = 0.85
        elif any(word in scenario_lower for word in ["ai", "machine learning", "algorithm", "automat", "model"]):
            position = "conditional"
            confidence = 0.65
        else:
            position = "neutral"
            confidence = 0.5

        # Determine AI risk level
        if any(word in scenario_lower for word in ["hiring", "credit", "criminal", "healthcare", "life-critical"]):
            ai_risk_level = "critical"
        elif any(word in scenario_lower for word in ["personal data", "decision-making", "scoring", "profiling"]):
            ai_risk_level = "high"
        elif any(word in scenario_lower for word in ["recommendation", "content", "optimization"]):
            ai_risk_level = "medium"
        else:
            ai_risk_level = "low"

        return AIGovernanceAgentResponse(
            agent_id="ai_governance",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "ethical_risk": (
                    "Algorithmic bias risk assessment identifies potential disparate impact "
                    "across protected attributes (race, gender, age, disability). Training data "
                    "representativeness must be verified — historical data often encodes systemic "
                    "biases. Fairness metrics (demographic parity, equalized odds, predictive "
                    "parity) must be tested pre-deployment and monitored continuously."
                ),
                "transparency_requirements": (
                    "Model explainability requirements depend on risk classification. For high-risk "
                    "applications, individual decision explanations (LIME/SHAP) are required. "
                    "Model cards documenting training data, performance metrics, and known limitations "
                    "must be published. Affected individuals must have right to explanation "
                    "and meaningful human review of adverse decisions."
                ),
                "governance_framework": (
                    "AI Ethics Board review required before deployment. Model risk management "
                    "classification per NIST AI RMF: Map, Measure, Manage, Govern. EU AI Act "
                    "risk tier assessment needed for regulatory compliance planning. Ongoing "
                    "monitoring with defined escalation thresholds and incident response "
                    "procedures must be established pre-deployment."
                ),
                "societal_impact": (
                    "Automated decision-making at scale affects thousands of individuals. "
                    "Disproportionate impact on vulnerable populations must be assessed. "
                    "Digital divide considerations — AI systems may disadvantage those with "
                    "less digital literacy. Long-term workforce displacement effects require "
                    "just transition planning. Public trust implications of AI deployment "
                    "in sensitive domains must be weighed."
                ),
                "ai_risk_level": ai_risk_level,
            },
            summary=(
                f"From an AI governance perspective, this proposal is {position} with "
                f"{confidence:.0%} confidence — responsible deployment requires verified "
                f"fairness testing and governance oversight before production use."
            ),
            rationale=(
                evidence_prefix +
                "From an AI ethics perspective, this proposal requires careful governance "
                "consideration. Any AI system that makes or influences decisions affecting "
                "individuals must meet responsible AI standards including fairness, "
                "transparency, accountability, and harm prevention. The risk level "
                "determines the intensity of governance required.\n\n"
                "The primary ethical concern is ensuring algorithmic fairness across "
                "protected attributes. Historical data used for training frequently "
                "encodes systemic biases that, if not detected and mitigated, result in "
                "discriminatory outcomes at scale. Pre-deployment bias testing using "
                "multiple fairness metrics is non-negotiable, and ongoing monitoring "
                "must detect performance degradation or emergent bias.\n\n"
                "From a governance standpoint, I recommend establishing clear "
                "accountability structures: an AI Ethics Board for pre-deployment review, "
                "model risk tiers with corresponding oversight levels, documented "
                "escalation procedures for identified harms, and regular third-party "
                "audits. The NIST AI Risk Management Framework provides an appropriate "
                "governance structure. Human oversight mechanisms must be proportionate "
                "to the risk level — high-risk applications require human-in-the-loop "
                "for all adverse decisions."
            ),
            risks=[
                "Algorithmic bias encoding historical discrimination — disparate impact on protected groups without pre-deployment fairness testing",
                "Lack of explainability in complex models creates accountability gaps and regulatory non-compliance risk (EU AI Act Article 13)",
                "Model drift and performance degradation over time without continuous monitoring may introduce emergent bias",
                "Absence of human oversight for high-stakes decisions violates responsible AI principles and emerging regulations",
            ],
            conditions=[
                "Complete bias and fairness audit across all protected attributes before production deployment",
                "Implement model explainability appropriate to risk tier — SHAP/LIME for individual decisions in high-risk applications",
                "Establish AI Ethics Board review process with documented approval for all high-risk AI deployments",
                "Deploy continuous monitoring with defined drift thresholds and automated alerting for fairness metric degradation",
            ],
            metrics_to_track=[
                "Fairness metrics (demographic parity, equalized odds) across all protected attributes — monthly measurement",
                "Model explainability coverage — percentage of decisions with available explanations",
                "Human override rate — frequency of human reviewers overturning AI decisions",
                "AI incident count and severity — track all identified harms or near-misses",
                "Time to detection for bias drift — target under 7 days for significant deviations",
            ],
            references_to=[],
        )
