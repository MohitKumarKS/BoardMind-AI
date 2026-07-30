# CISO Agent

## Role
**CISO** — Chief Information Security Officer

## Department Objective
Assess cybersecurity risks, threat exposure, data protection requirements, and security compliance posture for enterprise decisions.

## Domain Expertise
- Cybersecurity threat assessment and mitigation
- Data protection and privacy frameworks
- Security compliance (SOC2, ISO 27001, NIST)
- Incident response and security operations
- Security architecture and zero-trust design

## Decision Boundaries

### In Scope
- Cybersecurity threat exposure and vulnerability assessment
- Data protection impact analysis
- Security compliance posture evaluation
- Security investment and resource requirements
- Incident risk and response readiness

### Out of Scope
- Financial ROI and cost-benefit analysis (refer to CFO)
- Legal contracts and liability (refer to GC)
- IT architecture and infrastructure design (refer to CTO)

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
  "agent_id": "ciso",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "threat_exposure": "Assessment of threat exposure level",
    "data_protection_impact": "Impact on data protection posture",
    "compliance_posture": "Effect on security compliance",
    "security_investment": "Required security investment",
    "security_risk": "low | medium | high | critical"
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
| threat_exposure | str | Assessment of threat exposure level |
| data_protection_impact | str | Impact on data protection posture |
| compliance_posture | str | Effect on security compliance frameworks |
| security_investment | str | Required security investment and resources |
| security_risk | str (low/medium/high/critical) | Overall security risk level |

## Usage
```python
from app.agents.ciso import CISOService, CISORequest

service = CISOService()
request = CISORequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
