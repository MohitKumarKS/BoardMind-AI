# Business Analytics AI Agent (CDO)

An AI-powered Chief Data Officer agent that evaluates evidence strength, data availability, projection confidence, measurement frameworks, and benchmarks for business proposals.

## Project Overview

The Business Analytics AI Agent embodies an empirical, intellectually honest CDO who demands evidence before confidence. It challenges unsupported claims, identifies data gaps, provides statistical context via benchmarks, and proposes measurement frameworks.

## Problem Statement

Decision-making in organizations often lacks analytical rigor:
- **Unsupported projections** — bold claims without data backing
- **Confirmation bias** — positive signals overweighted, negatives explained away
- **Missing baselines** — no before/after comparison possible without pre-measurement
- **Survivorship bias** — benchmarks based on published successes, not base rates

## Solution

The Business Analytics AI Agent delivers:
- Evidence strength classification (strong / moderate / weak / insufficient)
- Data availability assessment for decision support
- Projection confidence rating based on assumption quality
- Key metrics and KPI frameworks for tracking success
- Industry benchmarks and base rates for context
- Concrete measurement plans with phased timelines and success criteria

## Agent Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Evidence Strength | How well-supported the proposal's claims are |
| Data Availability | Whether needed data exists or must be collected |
| Projection Confidence | Reliability of stated projections |
| Key Metrics | What should be measured to evaluate success |
| Benchmarks | Industry context and base rates for comparison |
| Measurement Plan | Phased plan for defining and tracking success |

## Features

- **Evidence Demanding** — Challenges unsupported claims with data requirements
- **Statistically Grounded** — Provides base rates and benchmark context
- **Intellectually Honest** — Says "we don't know" when evidence is insufficient
- **Measurement-Focused** — Always provides a concrete framework to track outcomes
- **Evidence Integration** — References uploaded datasets, citing specific figures
- **Retry & Fallback** — Graceful degradation on LLM failures

## Usage

```bash
curl -X POST http://localhost:8000/api/workspace/business_analytics \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "We project 185% ROI over 5 years from a $950M digital transformation with 18% revenue growth target.",
    "context": "Annual Revenue: $6.8B. Historical growth rate: 8-12%."
  }'
```

### Response Structure

```json
{
  "agent_id": "business_analytics",
  "position": "conditional",
  "confidence": 0.55,
  "domain_assessment": {
    "evidence_strength": "weak",
    "data_availability": "partially_available",
    "projection_confidence": "low",
    "key_metrics": ["Actual vs projected ROI quarterly", "Revenue growth rate"],
    "benchmarks": ["Industry median digital transformation ROI: 120-150%"]
  },
  "measurement_plan": "Phase 1 (Months 1-6): Establish baselines. Phase 2 (Months 7-12): Track leading indicators weekly. Phase 3 (Month 18): Full outcome assessment with confidence intervals."
}
```

## Project Structure

```
business_analytics/
├── __init__.py       # Package exports
├── prompt.py         # CDO system prompt with measurement focus
├── schema.py         # Pydantic models (evidence, data, projection enums)
├── service.py        # Agent service with retry logic
└── examples.py       # Few-shot examples
```

## Future Enhancements

- Integration with BI platforms (Tableau, Power BI, Looker)
- Automated statistical significance testing
- Bayesian prior updating from historical decision outcomes
- Data quality scoring from uploaded datasets
- Causal inference framework recommendations

## License

MIT License
