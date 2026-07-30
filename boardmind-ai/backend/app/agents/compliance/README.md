# Compliance Agent

## Role
**CCO** — Chief Compliance Officer

## Department Objective
Ensure regulatory compliance, governance framework adherence, audit readiness, and policy alignment for enterprise decisions.

## Domain Expertise
- Regulatory compliance frameworks (SOX, GDPR, HIPAA)
- Governance frameworks and corporate policies
- Audit readiness and internal controls
- Policy adherence and gap analysis
- Regulatory change management and horizon scanning

## Decision Boundaries

### In Scope
- Regulatory impact assessment
- Compliance gap identification
- Remediation effort estimation
- Audit readiness evaluation
- Policy adherence verification

### Out of Scope
- Security implementation and controls (refer to CISO)
- Legal strategy and litigation (refer to GC)
- Financial impact and cost analysis (refer to CFO)

## Input Schema
```json
{
  "scenario": "Business proposal text (min 20 chars)",
  "context": "Optional additional context"
}
```

## Output Schema
```json
{
  "agent_id": "compliance",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "regulatory_impact": "Assessment of regulatory implications",
    "compliance_gaps": "Identified compliance gaps",
    "remediation_effort": "Effort required for remediation",
    "audit_readiness": "Current audit readiness state",
    "compliance_status": "compliant | non_compliant | requires_review"
  },
  "summary": "One-sentence position statement",
  "rationale": "2-4 paragraphs of domain reasoning",
  "risks": ["Risk 1", "Risk 2", "Risk 3"],
  "conditions": ["Condition for support"],
  "metrics_to_track": ["KPI 1", "KPI 2"]
}
```

## Domain Assessment Fields
| Field | Type | Description |
|-------|------|-------------|
| regulatory_impact | str | Assessment of regulatory implications |
| compliance_gaps | str | Identified compliance gaps and deficiencies |
| remediation_effort | str | Effort required for compliance remediation |
| audit_readiness | str | Current state of audit readiness |
| compliance_status | str (compliant/non_compliant/requires_review) | Overall compliance status |

## Usage
```python
from app.agents.compliance import ComplianceService, ComplianceRequest

service = ComplianceService()
request = ComplianceRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
