# Customer Success Agent

## Role
**CCusO** — Chief Customer Officer

## Department Objective
Champion customer retention, satisfaction, NPS/CSAT optimization, and customer lifecycle management across the organization.

## Domain Expertise
- Customer retention and churn prevention
- Customer satisfaction measurement (NPS, CSAT, CES)
- Customer lifecycle management and journey mapping
- Voice of customer programs and feedback loops
- Customer success operations and health scoring

## Decision Boundaries

### In Scope
- Customer impact assessment
- Retention risk evaluation
- Satisfaction forecast modeling
- Support requirements estimation
- Customer risk classification

### Out of Scope
- Sales pipeline and revenue forecasting (refer to CRO)
- Marketing campaigns and brand strategy (refer to CMO)
- Pricing strategy and financial modeling (refer to CFO)

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
  "agent_id": "customer_success",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "customer_impact": "Assessment of impact on customers",
    "retention_risk": "Risk to customer retention",
    "satisfaction_forecast": "Projected effect on satisfaction metrics",
    "support_requirements": "Support resources needed",
    "customer_risk": "low | medium | high"
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
| customer_impact | str | Assessment of impact on customer base |
| retention_risk | str | Risk to customer retention rates |
| satisfaction_forecast | str | Projected effect on satisfaction metrics |
| support_requirements | str | Support resources and infrastructure needed |
| customer_risk | str (low/medium/high) | Overall customer risk level |

## Usage
```python
from app.agents.customer_success import CustomerSuccessService, CustomerSuccessRequest

service = CustomerSuccessService()
request = CustomerSuccessRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
