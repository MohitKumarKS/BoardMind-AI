# Product Agent

## Role
**CPO** — Chief Product Officer

## Department Objective
Guide product strategy, roadmap alignment, product-market fit assessment, and user experience decisions for the organization.

## Domain Expertise
- Product strategy and vision development
- Product roadmap planning and prioritization
- Product-market fit assessment and validation
- User experience and design thinking
- Build vs. buy decision frameworks

## Decision Boundaries

### In Scope
- Product-market fit evaluation
- Roadmap impact assessment
- User experience implications
- Build vs. buy analysis
- Feature feasibility classification

### Out of Scope
- Engineering implementation and technical architecture (refer to CTO)
- Pricing strategy and revenue modeling (refer to CFO)
- Marketing campaigns and go-to-market execution (refer to CMO)

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
  "agent_id": "product",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "product_market_fit": "Assessment of product-market fit",
    "roadmap_impact": "Impact on product roadmap",
    "user_experience": "Effect on user experience",
    "build_vs_buy": "Build vs. buy recommendation",
    "feasibility": "straightforward | moderate | complex | infeasible"
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
| product_market_fit | str | Assessment of product-market fit alignment |
| roadmap_impact | str | Impact on current product roadmap |
| user_experience | str | Effect on user experience and satisfaction |
| build_vs_buy | str | Build vs. buy recommendation and rationale |
| feasibility | str (straightforward/moderate/complex/infeasible) | Implementation feasibility level |

## Usage
```python
from app.agents.product import ProductService, ProductRequest

service = ProductService()
request = ProductRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
