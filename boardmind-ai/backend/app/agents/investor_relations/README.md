# Investor Relations Agent

## Role
**IRO** — Investor Relations Officer

## Department Objective
Manage shareholder communication, market perception, earnings impact analysis, and analyst relations for corporate transparency.

## Domain Expertise
- Shareholder communication and engagement
- Market perception and sentiment analysis
- Earnings impact and financial narrative
- Analyst relations and investor briefings
- Capital markets and valuation impact

## Decision Boundaries

### In Scope
- Market perception assessment
- Earnings impact evaluation
- Shareholder value analysis
- Communication strategy development
- Investor sentiment classification

### Out of Scope
- Internal finance and accounting (refer to CFO)
- Legal filings and SEC compliance (refer to GC)
- Product strategy and roadmap (refer to CPO)

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
  "agent_id": "investor_relations",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "market_perception": "Assessment of market perception impact",
    "earnings_impact": "Impact on earnings and financial narrative",
    "shareholder_value": "Effect on shareholder value",
    "communication_strategy": "Recommended communication approach",
    "investor_sentiment": "positive | neutral | negative | mixed"
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
| market_perception | str | Assessment of market perception impact |
| earnings_impact | str | Impact on earnings and financial narrative |
| shareholder_value | str | Effect on shareholder value creation |
| communication_strategy | str | Recommended communication approach |
| investor_sentiment | str (positive/neutral/negative/mixed) | Overall investor sentiment classification |

## Usage
```python
from app.agents.investor_relations import InvestorRelationsService, InvestorRelationsRequest

service = InvestorRelationsService()
request = InvestorRelationsRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
