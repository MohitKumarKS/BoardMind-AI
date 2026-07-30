"""Compliance Officer Agent service.

This module provides the ComplianceAgentService which:
1. Receives a business proposal
2. Builds the Compliance prompt
3. Invokes the configured LLM (or falls back to mock)
4. Validates the response against the schema
5. Returns a ComplianceAgentResponse object
"""

import json
import logging
from typing import Optional

from .prompt import COMPLIANCE_SYSTEM_PROMPT, build_compliance_prompt
from .schema import ComplianceAgentRequest, ComplianceAgentResponse
from app.agents.llm_provider import (
    get_provider,
    BaseLLMProvider,
    LLMError,
    LLMNotConfiguredError,
)

logger = logging.getLogger(__name__)


class ComplianceAgentService:
    """Service for the Compliance Agent in Department Workspace mode.

    Usage:
        service = ComplianceAgentService()
        response = await service.analyze(request)
    """

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: ComplianceAgentRequest) -> ComplianceAgentResponse:
        """Analyze a business proposal from the CCO perspective."""
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_compliance_prompt(request.scenario, request.context)
        logger.info("Invoking LLM for Compliance Agent analysis")

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="compliance",
            llm_generate=self.llm.generate,
            system_prompt=COMPLIANCE_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> ComplianceAgentResponse:
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

        data["agent_id"] = "compliance"
        data["round"] = 1
        data["references_to"] = []

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return ComplianceAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: ComplianceAgentRequest) -> ComplianceAgentResponse:
        """Generate a realistic mock response for development and testing."""
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "compliance")

        # Determine position based on scenario signals
        if any(word in scenario_lower for word in ["compliant", "audit-ready", "certified", "documented"]):
            position = "support"
            confidence = 0.8
        elif any(word in scenario_lower for word in ["violate", "ignore", "bypass", "skip compliance", "without approval"]):
            position = "oppose"
            confidence = 0.9
        elif any(word in scenario_lower for word in ["data", "international", "customer", "process", "collect"]):
            position = "conditional"
            confidence = 0.7
        else:
            position = "neutral"
            confidence = 0.5

        # Determine compliance status
        if any(word in scenario_lower for word in ["violate", "breach", "non-compliant", "penalty"]):
            compliance_status = "non_compliant"
        elif any(word in scenario_lower for word in ["compliant", "certified", "approved"]):
            compliance_status = "compliant"
        else:
            compliance_status = "requires_review"

        return ComplianceAgentResponse(
            agent_id="compliance",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "regulatory_impact": (
                    "This proposal touches multiple regulatory frameworks: "
                    "GDPR (if EU data subjects involved — Articles 6, 13, 14, 35), "
                    "CCPA/CPRA (California residents — right to know, delete, opt-out), "
                    "and potentially SOX Section 404 (internal controls over financial "
                    "reporting if it affects financial data flows). Industry-specific "
                    "regulations (HIPAA, PCI-DSS) may apply depending on data types."
                ),
                "compliance_gaps": (
                    "Preliminary gap assessment identifies: (1) Data Protection Impact "
                    "Assessment (DPIA) not yet completed for new processing activities, "
                    "(2) Privacy notices may require updates to reflect new data usage, "
                    "(3) Data processing agreements with third parties need review for "
                    "adequacy, (4) Retention and deletion policies undefined for new "
                    "data categories. Gap severity: moderate — all remediable."
                ),
                "remediation_effort": (
                    "Estimated 6-10 weeks total remediation effort: DPIA completion "
                    "(2-3 weeks), privacy notice updates (1 week legal review), "
                    "DPA amendments with third parties (3-4 weeks negotiation), "
                    "policy documentation and staff training (2 weeks). "
                    "Resource requirement: 0.5 FTE compliance + legal support."
                ),
                "audit_readiness": (
                    "Current certification cycle (SOC2 Type II) can accommodate "
                    "this change if remediation completes 30 days before next audit "
                    "window. No impact on ISO27001 certification if security controls "
                    "are maintained. Recommend pre-audit readiness check with external "
                    "auditor to confirm scope alignment."
                ),
                "compliance_status": compliance_status,
            },
            summary=(
                f"From a compliance perspective, this proposal is {position} — "
                f"{'regulatory requirements are achievable with identified remediation' if position in ('support', 'conditional') else 'regulatory assessment needed before proceeding'} "
                f"with {confidence:.0%} confidence."
            ),
            rationale=(
                evidence_prefix +
                "From a regulatory compliance perspective, this proposal introduces "
                "obligations under multiple frameworks that must be addressed before "
                "implementation. The good news is that none of the identified gaps "
                "represent fundamental blockers — all are remediable with proper "
                "planning and adequate timeline.\n\n"
                "The primary compliance concern is the interaction between data "
                "processing activities and applicable privacy regulations. GDPR "
                "Article 35 requires a Data Protection Impact Assessment before "
                "processing that is likely to result in high risk to individuals. "
                "CCPA/CPRA requires specific disclosures and opt-out mechanisms. "
                "These are procedural requirements, not prohibitions — compliance "
                "is achievable but requires upfront investment in documentation "
                "and process.\n\n"
                "I recommend proceeding with compliance workstream running in "
                "parallel with technical implementation, with a hard gate: no "
                "production deployment until DPIA is complete and all identified "
                "gaps are remediated. This approach avoids unnecessary delay while "
                "ensuring regulatory compliance at the point of customer impact."
            ),
            risks=[
                "GDPR enforcement action — failure to complete DPIA before processing constitutes a procedural violation (fines up to 2% of annual turnover)",
                "Audit finding — unaddressed compliance gaps discovered during SOC2 audit could result in qualified opinion or certification delay",
                "Cross-border data transfer issues — if data flows to non-adequate jurisdictions without proper safeguards (SCCs, BCRs), creates immediate violation",
                "Third-party compliance chain — vendor non-compliance becomes our liability under data controller responsibilities",
            ],
            conditions=[
                "Complete Data Protection Impact Assessment before any new data processing begins",
                "Update privacy notices and obtain fresh consent where required by regulation",
                "Execute updated Data Processing Agreements with all affected third parties",
                "Conduct pre-audit readiness review to confirm alignment with SOC2 scope",
            ],
            metrics_to_track=[
                "Compliance gap closure rate — target 100% of identified gaps closed before launch",
                "Regulatory inquiry response time — maintain <48 hour SLA for any regulator requests",
                "Policy attestation completion — 100% of affected staff trained and attested within 30 days",
                "Audit finding count — target zero material findings related to new initiative",
                "Data subject request fulfillment — maintain <30 day response time per GDPR Article 12",
            ],
            references_to=[],
        )
