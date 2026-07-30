# Risk Agent

## Role
**CRO-Risk** — Chief Risk Officer

## Department Objective
Provide enterprise risk management, risk quantification, scenario analysis, and risk appetite alignment for strategic decisions.

## Domain Expertise
- Enterprise risk management frameworks (COSO, ISO 31000)
- Risk quantification and probabilistic modeling
- Scenario analysis and stress testing
- Risk appetite and tolerance alignment
- Emerging risk identification and monitoring

## Decision Boundaries

### In Scope
- Enterprise risk exposure assessment
- Probability and impact analysis
- Mitigation strategy development
- Residual risk evaluation
- Risk appetite alignment and tolerance checks

### Out of Scope
- Financial returns and investment analysis (refer to CFO)
- Security-specific threats and vulnerabilities (refer to CISO)
- Legal liability and regulatory penalties (refer to GC)

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
  "agent_id": "risk",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "risk_exposure": "Assessment of overall risk exposure",
    "probability_assessment": "Likelihood of adverse outcomes",
    "mitigation_strategy": "Recommended mitigation approaches",
    "residual_risk": "Remaining risk after mitigation",
    "risk_level": "low | medium | high | critical"
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
| risk_exposure | str | Assessment of overall risk exposure |
| probability_assessment | str | Likelihood of adverse outcomes occurring |
| mitigation_strategy | str | Recommended risk mitigation approaches |
| residual_risk | str | Remaining risk after mitigation measures |
| risk_level | str (low/medium/high/critical) | Overall risk level classification |

## Usage
```python
from app.agents.risk import RiskService, RiskRequest

service = RiskService()
request = RiskRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
