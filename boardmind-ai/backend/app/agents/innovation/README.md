# Innovation Agent

## Role
**CIO-Inn** — Chief Innovation Officer

## Department Objective
Drive R&D strategy, emerging technology evaluation, innovation pipeline management, and intellectual property development.

## Domain Expertise
- R&D strategy and innovation management
- Emerging technology assessment and adoption
- Innovation pipeline and portfolio management
- Patent strategy and intellectual property
- Technology readiness level (TRL) evaluation

## Decision Boundaries

### In Scope
- Innovation potential assessment
- Technology readiness evaluation
- Research requirements identification
- IP opportunity analysis
- Innovation risk classification

### Out of Scope
- Production engineering and deployment (refer to CTO)
- Financial modeling and investment returns (refer to CFO)
- Market positioning and brand strategy (refer to CMO)

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
  "agent_id": "innovation",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "innovation_potential": "Assessment of innovation potential",
    "technology_readiness": "Technology readiness level evaluation",
    "research_requirements": "Required research and development effort",
    "ip_opportunity": "Intellectual property opportunities",
    "innovation_risk": "low | medium | high"
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
| innovation_potential | str | Assessment of innovation potential and novelty |
| technology_readiness | str | Technology readiness level evaluation |
| research_requirements | str | Required research and development effort |
| ip_opportunity | str | Intellectual property opportunities |
| innovation_risk | str (low/medium/high) | Overall innovation risk level |

## Usage
```python
from app.agents.innovation import InnovationService, InnovationRequest

service = InnovationService()
request = InnovationRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
