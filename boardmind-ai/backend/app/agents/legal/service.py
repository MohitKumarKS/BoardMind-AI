"""Legal Agent service."""

import json
import logging
from typing import Optional

from app.agents.llm_provider import get_provider, BaseLLMProvider, LLMError, LLMNotConfiguredError
from .prompt import LEGAL_SYSTEM_PROMPT, build_legal_prompt
from .schema import LegalAgentRequest, LegalAgentResponse

logger = logging.getLogger(__name__)


class LegalAgentService:
    """Service for the Legal Agent in Department Workspace mode."""

    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm = llm_provider or get_provider()

    async def analyze(self, request: LegalAgentRequest) -> LegalAgentResponse:
        if not self.llm.is_configured:
            logger.info("LLM not configured — returning mock response")
            return self._generate_mock_response(request)

        user_prompt = build_legal_prompt(request.scenario, request.context)

        from app.agents.retry import retry_llm_call
        return await retry_llm_call(
            agent_id="legal",
            llm_generate=self.llm.generate,
            system_prompt=LEGAL_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            parse_fn=self._parse_and_validate,
            fallback_fn=lambda: self._generate_mock_response(request),
        )

    def _parse_and_validate(self, raw_response: str) -> LegalAgentResponse:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines[1:] if l.strip() != "```"]
            cleaned = "\n".join(lines)

        data = json.loads(cleaned)
        data["agent_id"] = "legal"
        data["round"] = 1
        data["references_to"] = []

        # Normalize enum fields that the LLM may return as descriptive text
        if "domain_assessment" in data and isinstance(data["domain_assessment"], dict):
            da = data["domain_assessment"]

            # Normalize ip_implications → must be "none", "minor", or "significant"
            ip = str(da.get("ip_implications", "none")).lower()
            if "significant" in ip:
                da["ip_implications"] = "significant"
            elif "minor" in ip:
                da["ip_implications"] = "minor"
            else:
                da["ip_implications"] = "none"

            # Normalize compliance_status
            cs = str(da.get("compliance_status", "requires_review")).lower()
            if "non-compliant" in cs or "non_compliant" in cs:
                da["compliance_status"] = "non-compliant"
            elif "compliant" in cs and "non" not in cs:
                da["compliance_status"] = "compliant"
            else:
                da["compliance_status"] = "requires_review"

            # Normalize risk_level
            rl = str(da.get("risk_level", "medium")).lower()
            if "critical" in rl:
                da["risk_level"] = "critical"
            elif "high" in rl:
                da["risk_level"] = "high"
            elif "low" in rl:
                da["risk_level"] = "low"
            else:
                da["risk_level"] = "medium"

        from app.agents.response_normalizer import normalize_agent_response
        data = normalize_agent_response(data)

        return LegalAgentResponse.model_validate(data)

    def _generate_mock_response(self, request: LegalAgentRequest) -> LegalAgentResponse:
        from app.agents.evidence_extractor import extract_evidence_facts, build_evidence_rationale_prefix

        scenario_lower = request.scenario.lower()
        context = request.context or ""
        facts = extract_evidence_facts(context)
        evidence_prefix = build_evidence_rationale_prefix(facts, "legal")

        if any(w in scenario_lower for w in ["gdpr", "hipaa", "privacy", "compliance", "regulated"]):
            position = "conditional"
            confidence = 0.75
            compliance_status = "requires_review"
            risk_level = "high"
        elif any(w in scenario_lower for w in ["patent", "copyright", "ip", "license", "trademark"]):
            position = "conditional"
            confidence = 0.7
            compliance_status = "requires_review"
            risk_level = "medium"
            ip_implications = "significant"
        elif any(w in scenario_lower for w in ["contract", "partner", "vendor", "agreement"]):
            position = "conditional"
            confidence = 0.65
            compliance_status = "requires_review"
            risk_level = "medium"
        else:
            position = "conditional"
            confidence = 0.6
            compliance_status = "requires_review"
            risk_level = "medium"

        # Determine regulatory bodies based on scenario content
        regulatory_bodies = ["General corporate law"]
        if any(w in scenario_lower for w in ["data", "privacy", "personal", "user"]):
            regulatory_bodies.append("Data protection authorities (GDPR/CCPA)")
        if any(w in scenario_lower for w in ["europe", "eu", "international"]):
            regulatory_bodies.append("EU regulatory framework")
        if any(w in scenario_lower for w in ["health", "medical", "patient"]):
            regulatory_bodies.append("HIPAA / HHS")
        if any(w in scenario_lower for w in ["financial", "payment", "banking"]):
            regulatory_bodies.append("Financial regulators (SEC/FCA)")
        if any(w in scenario_lower for w in ["employ", "hire", "worker", "labor"]):
            regulatory_bodies.append("Employment law / DOL")

        ip_implications = "none"
        if any(w in scenario_lower for w in ["patent", "ip", "copyright", "proprietary", "algorithm"]):
            ip_implications = "significant"
        elif any(w in scenario_lower for w in ["software", "technology", "platform"]):
            ip_implications = "minor"

        return LegalAgentResponse(
            agent_id="legal",
            round=1,
            position=position,
            confidence=confidence,
            domain_assessment={
                "compliance_status": compliance_status,
                "risk_level": risk_level,
                "liability_exposure": (
                    "Moderate liability exposure requiring standard contractual protections. "
                    "Potential exposure range: $100K-$2M depending on scope of data handling, "
                    "regulatory jurisdiction, and contractual obligations involved."
                ),
                "regulatory_bodies": regulatory_bodies,
                "ip_implications": ip_implications,
            },
            summary=(
                "This proposal requires legal review and specific safeguards before "
                "proceeding — the compliance pathway exists but must be formally established."
            ),
            rationale=(
                evidence_prefix +
                "From a legal perspective, this proposal presents manageable but non-trivial "
                "risk that requires structured mitigation. The primary concern is ensuring "
                "compliance with applicable regulatory frameworks before operational "
                "commitments are made. Proceeding without formal legal review creates "
                "potential exposure that, while unlikely to materialize immediately, could "
                "result in significant liability if regulatory scrutiny occurs.\n\n"
                "The contractual dimensions require attention. Any new business relationships, "
                "vendor engagements, or customer commitments arising from this proposal "
                "should be documented with appropriate protections: limitation of liability "
                "clauses, indemnification provisions, and clear termination rights. Standard "
                "form agreements may be insufficient given the scope described.\n\n"
                "I note that data handling and privacy implications exist here. Depending on "
                "the jurisdictions involved and the nature of data processed, specific "
                "compliance frameworks (GDPR, CCPA, or sector-specific regulations) may "
                "apply. These should be identified and addressed in the compliance plan "
                "before any data processing begins.\n\n"
                "My recommendation is conditional approval with the safeguards outlined below. "
                "The legal risk is manageable, but only if the compliance framework is "
                "established proactively rather than retrofitted after launch."
            ),
            risks=[
                "Regulatory non-compliance risk if applicable frameworks are not identified and addressed before launch",
                "Contractual liability exposure if agreements lack adequate protection clauses and limitation provisions",
                "Data privacy violation risk if personal data handling does not comply with applicable jurisdictional requirements",
                "IP exposure if proprietary information sharing lacks adequate NDA and licensing protections",
            ],
            conditions=[
                "Complete regulatory compliance assessment for all applicable jurisdictions before operational launch",
                "Engage external legal counsel for specialized regulatory areas outside general corporate law",
                "Establish documented compliance framework with assigned ownership and review cadence",
                "Obtain formal sign-off from Legal on all customer-facing agreements and vendor contracts",
            ],
            required_safeguards=[
                "Draft and execute appropriate contractual protections (limitation of liability, indemnification, IP assignment)",
                "Implement data processing agreements (DPAs) compliant with applicable privacy regulations",
                "Establish regulatory compliance monitoring with quarterly review and escalation path",
                "Create incident response protocol for potential regulatory inquiries or data breach scenarios",
                "Document all legal assumptions and obtain written confirmation of compliance posture",
            ],
            references_to=[],
        )
