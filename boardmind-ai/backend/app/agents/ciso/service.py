"""CISO Agent service.

This module provides the CISOAgentService which:
1. Receives a business proposal
2. Builds the CISO prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a CISOAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import CISO_SYSTEM_PROMPT, build_ciso_prompt
from .schema import CISOAgentRequest, CISOAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class CISOAgentService:
    """Service for the CISO Agent in Department Workspace mode.

    Usage:
        service = CISOAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: CISOAgentRequest) -> CISOAgentResponse:
        """Analyze a business proposal from the CISO perspective."""
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_ciso_prompt(request.scenario, request.context)
        logger.info("Invoking LLM for CISO Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="ciso",
            llm_generate=self.llm.generate,
            system_prompt=CISO_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> CISOAgentResponse:
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

        data["agent_id"] = "ciso"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return CISOAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: CISOAgentRequest) -> CISOAgentResponse:
        """Generate a realistic mock response for development and testing."""
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "ciso")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["encrypt", "secure", "protect", "zero-trust", "audit"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["public", "unencrypted", "bypass", "shortcut", "skip security"]):
            position = "oppose"
            confidence = 0.85
        elif any(word in scenario_lower for word in ["cloud", "migrate", "third-party", "vendor", "api"]):
            position = "conditional"
            confidence = 0.7
        else:
            position = "neutral"
            confidence = 0.5

        # Determine security risk level
        if any(word in scenario_lower for word in ["pii", "credentials", "healthcare", "financial data", "breach"]):
            security_risk = "critical"
        elif any(word in scenario_lower for word in ["customer data", "cloud", "international", "third-party"]):
            security_risk = "high"
        elif any(word in scenario_lower for word in ["internal", "pilot", "sandbox"]):
            security_risk = "low"
        else:
            security_risk = "medium"

        return CISOAgentResponse(
            agent_id="ciso",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "threat_exposure": (
                    "This proposal introduces new attack surface through additional "
                    "integration points and data flows. Specific threats include: "
                    "unauthorized access via new API endpoints, data exfiltration "
                    "risk through expanded network paths, and supply chain risk "
                    "from new vendor dependencies."
                ),
                "data_protection_impact": (
                    "Sensitive data handling is affected — new data flows require "
                    "encryption in transit (TLS 1.3) and at rest (AES-256). "
                    "Data classification review needed for any new data stores. "
                    "Privacy impact assessment required under GDPR Article 35 "
                    "if personal data processing changes."
                ),
                "compliance_posture": (
                    "Current SOC2 Type II certification may require scope extension. "
                    "ISO27001 Annex A controls need mapping to new architecture. "
                    "No immediate compliance violations identified, but gap "
                    "assessment required before production deployment."
                ),
                "security_investment": (
                    "Estimated security controls cost: $50K-$150K for initial "
                    "implementation (WAF, SIEM integration, penetration testing). "
                    "Ongoing: $20K-$40K/month for monitoring, vulnerability scanning, "
                    "and security operations coverage of new attack surface."
                ),
                "security_risk": security_risk,
            },
            summary=(
                f"From a CISO perspective, this proposal is {position} — "
                f"{'security controls can adequately mitigate identified threats' if position == 'support' else 'specific security controls must be implemented before proceeding'} "
                f"with {confidence:.0%} confidence."
            ),
            rationale=(
                evidence_prefix +
                "From a security perspective, this proposal introduces manageable "
                "but non-trivial risk to our security posture. The primary concern "
                "is the expanded attack surface — every new integration point, data "
                "flow, and vendor dependency represents a potential vector for "
                "compromise. Our threat model must be updated to reflect these changes.\n\n"
                "Data protection is the highest-priority consideration. Any changes "
                "to how we collect, process, store, or transmit sensitive data must "
                "maintain our defense-in-depth approach. I require encryption at all "
                "layers, strict access controls following least-privilege principles, "
                "and comprehensive audit logging for all data access operations.\n\n"
                "Compliance impact is moderate — our current SOC2 and ISO27001 "
                "certifications can accommodate this change with proper documentation "
                "and control implementation. However, I will not approve production "
                "deployment without a completed security assessment, penetration test, "
                "and updated risk register entries."
            ),
            risks=[
                "Expanded attack surface through new API endpoints and integration points increases exploitation probability by estimated 15-25%",
                "Third-party vendor dependency introduces supply chain risk — vendor security posture must be validated",
                "Data-in-transit exposure during migration or integration windows creates temporary vulnerability",
                "Insufficient access controls on new components could enable lateral movement in case of breach",
            ],
            conditions=[
                "Complete threat modeling and security architecture review before development begins",
                "Penetration testing of all new components before production deployment",
                "Vendor security assessment (SOC2 report review, security questionnaire) for any new third parties",
                "Implement monitoring and alerting for all new data flows within existing SIEM",
            ],
            metrics_to_track=[
                "Mean Time to Detect (MTTD) for security events in new components — target <15 minutes",
                "Vulnerability scan findings — target zero critical/high within 30 days of deployment",
                "Security incident rate — monitor for increase above baseline after launch",
                "Compliance audit findings related to new scope — target zero major findings",
                "Third-party risk score — maintain above 80/100 on security rating platforms",
            ],
            references_to=[],
        )
