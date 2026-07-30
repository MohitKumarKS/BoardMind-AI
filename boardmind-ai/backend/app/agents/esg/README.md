# ESG Agent

## Role
**ESG Officer** — ESG & Sustainability Officer

## Department Objective
Evaluate environmental sustainability, social responsibility, governance practices, and ESG reporting alignment (GRI, SASB, TCFD) for enterprise decisions.

## Domain Expertise
- Environmental sustainability and carbon footprint analysis
- Social responsibility and stakeholder impact
- Corporate governance and ethical practices
- ESG reporting frameworks (GRI, SASB, TCFD)
- Sustainable development goals (SDG) alignment

## Decision Boundaries

### In Scope
- Environmental impact assessment
- Social impact evaluation
- Governance implications analysis
- Sustainability scoring and benchmarking
- ESG risk classification

### Out of Scope
- Financial ROI and investment returns (refer to CFO)
- Legal specifics and regulatory penalties (refer to GC)
- IT infrastructure and technology systems (refer to CTO)

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
  "agent_id": "esg",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "environmental_impact": "Assessment of environmental implications",
    "social_impact": "Impact on social responsibility",
    "governance_implications": "Governance and ethical considerations",
    "sustainability_score": "Sustainability scoring assessment",
    "esg_risk": "low | medium | high | critical"
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
| environmental_impact | str | Assessment of environmental implications |
| social_impact | str | Impact on social responsibility and communities |
| governance_implications | str | Governance and ethical considerations |
| sustainability_score | str | Sustainability scoring and benchmarking |
| esg_risk | str (low/medium/high/critical) | Overall ESG risk level |

## Usage
```python
from app.agents.esg import ESGService, ESGRequest

service = ESGService()
request = ESGRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
