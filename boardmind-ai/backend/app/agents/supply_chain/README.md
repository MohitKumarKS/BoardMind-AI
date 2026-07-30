# Supply Chain Agent

## Role
**CSCO** — Chief Supply Chain Officer

## Department Objective
Manage supply chain operations, procurement strategy, logistics optimization, and vendor risk assessment for enterprise resilience.

## Domain Expertise
- Supply chain management and optimization
- Procurement strategy and vendor management
- Logistics and distribution planning
- Vendor risk assessment and diversification
- Supply chain resilience and continuity planning

## Decision Boundaries

### In Scope
- Supply chain impact assessment
- Vendor dependency analysis
- Logistics complexity evaluation
- Procurement needs identification
- Operational risk classification

### Out of Scope
- Financial accounting and cost allocation (refer to CFO)
- Technology infrastructure and systems (refer to CTO)
- Legal contracts and vendor agreements (refer to GC)

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
  "agent_id": "supply_chain",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "supply_chain_impact": "Assessment of supply chain implications",
    "vendor_dependency": "Vendor dependency and concentration risk",
    "logistics_complexity": "Logistics and distribution complexity",
    "procurement_needs": "Procurement requirements and sourcing",
    "operational_risk": "low | medium | high | critical"
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
| supply_chain_impact | str | Assessment of supply chain implications |
| vendor_dependency | str | Vendor dependency and concentration risk |
| logistics_complexity | str | Logistics and distribution complexity |
| procurement_needs | str | Procurement requirements and sourcing needs |
| operational_risk | str (low/medium/high/critical) | Overall operational risk level |

## Usage
```python
from app.agents.supply_chain import SupplyChainService, SupplyChainRequest

service = SupplyChainService()
request = SupplyChainRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
