# Human Resources AI Agent (CHRO)

An AI-powered Chief Human Resources Officer agent that evaluates workforce impact, skill gaps, organizational change complexity, cultural implications, and change management requirements for business proposals.

## Project Overview

The HR AI Agent embodies the empathetic yet strategic CHRO perspective. It evaluates proposals through the lens of people impact — understanding that every organizational change has human consequences that must be planned for, communicated transparently, and supported through transition.

## Problem Statement

People impact assessment in business decisions often fails due to:
- **Afterthought treatment** — HR considerations added after technical and financial decisions are made
- **Underestimated change burden** — organizations absorbing more change than they can sustain
- **Skill gap blindness** — assuming existing teams can pivot without training investment
- **Culture erosion** — rapid change degrading organizational values and engagement

## Solution

The HR AI Agent delivers:
- Headcount change classification (hiring / reduction / redeployment / none)
- Skill gap severity assessment with development timeline
- Organizational culture impact prediction
- Change management complexity evaluation
- Specific change management needs and readiness requirements
- People-first conditions that must be met for sustainable execution

## Agent Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Headcount Planning | Whether hiring, reduction, or redeployment is needed |
| Skill Gap Analysis | Severity of gaps and time to address them |
| Culture Impact | Effect on organizational values and engagement |
| Change Complexity | How difficult the organizational transition will be |
| Readiness Timeline | How long before people are prepared |
| Change Management | Specific actions needed to support the transition |

## Features

- **People-First Perspective** — Every recommendation considers human impact
- **Change Complexity Scoring** — Realistic assessment of organizational readiness
- **Culture Sensitivity** — Flags risks to values, engagement, and retention
- **Actionable Needs** — Specific change management actions, not vague recommendations
- **Evidence Integration** — References workforce data when uploaded
- **Retry & Fallback** — Graceful degradation on LLM failures

## Usage

```bash
curl -X POST http://localhost:8000/api/workspace/hr \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "We plan to reskill 9,000 employees for digital roles while automating 5% of the workforce over 24 months."
  }'
```

### Response Structure

```json
{
  "agent_id": "hr",
  "position": "conditional",
  "confidence": 0.65,
  "domain_assessment": {
    "headcount_change": "redeployment",
    "skill_gap": "significant",
    "culture_impact": "negative",
    "change_complexity": "high",
    "timeline_to_readiness": "12-18 months for full organizational readiness"
  },
  "change_management_needs": [
    "Executive communication explaining the 'why' before the 'what'",
    "Manager enablement sessions with talking points for team conversations",
    "Skills assessment for all impacted roles with individual development plans",
    "Anonymous pulse surveys to monitor morale during transition"
  ]
}
```

## Project Structure

```
hr/
├── __init__.py       # Package exports
├── prompt.py         # CHRO system prompt
├── schema.py         # Pydantic models (headcount, skill gap, culture enums)
├── service.py        # Agent service with retry logic
└── examples.py       # Few-shot examples
```

## Future Enhancements

- Integration with HRIS systems (Workday, BambooHR)
- Employee sentiment analysis from survey data
- Skills taxonomy mapping and gap quantification
- Change readiness scoring based on historical transitions
- Attrition risk modeling for affected populations

## License

MIT License
