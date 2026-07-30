# Strategy Agent

## Role
**CSO** — Chief Strategy Officer

## Department Objective
Drive corporate strategy, competitive analysis, market positioning, and long-term strategic planning for enterprise growth.

## Domain Expertise
- Corporate strategy development and execution
- Competitive analysis and market intelligence
- Market positioning and differentiation
- Long-term strategic planning and roadmapping
- Mergers, acquisitions, and strategic partnerships

## Decision Boundaries

### In Scope
- Market opportunity assessment
- Competitive advantage analysis
- Strategic fit evaluation
- Execution complexity estimation
- Strategic priority classification

### Out of Scope
- Financial modeling and projections (refer to CFO)
- Technology implementation and architecture (refer to CTO)
- Legal and regulatory specifics (refer to GC)
- Operational execution and logistics (refer to COO)

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
  "agent_id": "strategy",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "market_opportunity": "Assessment of market opportunity size and timing",
    "competitive_advantage": "Impact on competitive positioning",
    "strategic_fit": "Alignment with corporate strategy",
    "execution_complexity": "Complexity of strategic execution",
    "strategic_priority": "low | medium | high | critical"
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
| market_opportunity | str | Assessment of market opportunity size and timing |
| competitive_advantage | str | Impact on competitive positioning |
| strategic_fit | str | Alignment with overall corporate strategy |
| execution_complexity | str | Complexity of strategic execution |
| strategic_priority | str (low/medium/high/critical) | Strategic priority classification |

## Usage
```python
from app.agents.strategy import StrategyService, StrategyRequest

service = StrategyService()
request = StrategyRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
