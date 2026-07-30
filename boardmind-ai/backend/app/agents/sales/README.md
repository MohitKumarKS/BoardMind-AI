# Sales AI Agent (CRO)

An AI-powered Chief Revenue Officer agent that evaluates revenue upside, pipeline impact, deal cycle effects, competitive positioning in deals, and customer relationship implications of business proposals.

## Project Overview

The Sales AI Agent embodies a revenue-focused CRO who protects existing pipeline while evaluating new opportunity. It analyzes proposals through the lens of quota impact, customer trust, team capacity, and competitive deal dynamics — always ensuring that commitments to existing customers are honored while pursuing growth.

## Problem Statement

Revenue impact assessment of business decisions often fails due to:
- **Pipeline disruption blindness** — not accounting for how changes affect in-flight deals
- **Customer trust erosion** — existing accounts deprioritized for new initiatives
- **Team capacity ignored** — sales teams stretched without enablement or headcount
- **Competitive vulnerability** — gaps created while teams retool for new approaches

## Solution

The Sales AI Agent delivers:
- Revenue upside quantification with timeline and deal count estimates
- Revenue-at-risk identification for pipeline disruption scenarios
- Pipeline impact classification (new pipeline / acceleration / disruption)
- Deal cycle effect assessment (shorter / longer / unchanged)
- Competitive positioning in active deals
- Customer relationship impact analysis with key account communication plans

## Agent Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Revenue Upside | Projected additional ARR with deal count and timeline |
| Revenue Risk | Pipeline revenue at risk from disruption or confusion |
| Pipeline Impact | Effect on sales pipeline health and velocity |
| Deal Cycle | Whether deal closure timeline changes |
| Competitive Effect | How this helps or hurts in competitive deals |
| Customer Impact | Effect on key account relationships and trust |

## Features

- **Pipeline Protection** — Prioritizes protecting committed deals
- **Revenue Quantification** — Specific ARR projections with assumptions
- **Customer-First** — Ensures key accounts hear changes from us first
- **Enablement Requirements** — Identifies training and materials needs
- **Evidence Integration** — References uploaded sales data and forecasts
- **Retry & Fallback** — Graceful degradation on LLM failures

## Usage

```bash
curl -X POST http://localhost:8000/api/workspace/sales \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "We are launching a new AI-powered analytics product at $2,000/month targeting mid-market companies alongside our existing enterprise product line."
  }'
```

### Response Structure

```json
{
  "agent_id": "sales",
  "position": "support",
  "confidence": 0.75,
  "domain_assessment": {
    "revenue_upside": "Estimated $1.2M additional ARR within 12 months (50 new deals at $24K ACV)",
    "revenue_risk": "Potential $400K at risk from enterprise customer confusion during transition",
    "pipeline_impact": "new pipeline",
    "deal_cycle_effect": "unchanged",
    "competitive_effect": "advantage"
  },
  "customer_impact": "Key enterprise accounts need proactive executive outreach. New mid-market prospects benefit from clear value prop. Overall positive if communication is prioritized."
}
```

## Project Structure

```
sales/
├── __init__.py       # Package exports
├── prompt.py         # CRO system prompt
├── schema.py         # Pydantic models (pipeline, deal cycle, competitive enums)
├── service.py        # Agent service with retry logic
└── examples.py       # Few-shot examples
```

## Future Enhancements

- Integration with CRM systems (Salesforce, HubSpot)
- Pipeline velocity modeling based on historical data
- Win/loss analysis correlation with proposal characteristics
- Territory and quota impact modeling
- Customer health score integration

## License

MIT License
