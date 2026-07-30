# Operations AI Agent (COO)

An AI-powered Chief Operating Officer agent that evaluates execution complexity, resource requirements, capacity constraints, dependencies, and implementation phasing for business proposals.

## Project Overview

The Operations AI Agent thinks like a pragmatic COO focused on execution feasibility. It answers the fundamental question: "Can we actually deliver this, and what does it take?" It evaluates proposals through operational capacity, resource availability, dependency management, and phased execution planning.

## Problem Statement

Operational planning for new initiatives often fails due to:
- **Optimistic timelines** — ignoring dependencies, ramp-up time, and resource contention
- **Capacity blindness** — not accounting for existing team commitments
- **Dependency chains** — critical-path items not identified until they slip
- **Missing phase gates** — no checkpoints to validate assumptions before committing further

## Solution

The Operations AI Agent delivers:
- Execution complexity classification (low/medium/high)
- Realistic timeline estimates with buffer for uncertainty
- Resource requirements (people, tools, vendors)
- Capacity impact assessment (within capacity / stretch / overload)
- Critical dependency identification
- Phased implementation plan with readiness gates

## Agent Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Execution Complexity | How hard this is to deliver operationally |
| Timeline Estimation | Realistic duration accounting for dependencies and ramp-up |
| Resource Planning | Who and what is needed (headcount, tools, vendors) |
| Capacity Assessment | Whether current teams can absorb this work |
| Dependency Mapping | Critical-path items that block progress |
| Phased Delivery | Implementation broken into stages with gates |

## Features

- **Realistic Timelines** — Includes buffer for dependency resolution and ramp-up
- **Capacity-Aware** — Accounts for existing team commitments
- **Dependency Identification** — Flags cross-functional blockers
- **Phased Execution** — Concrete phases with go/no-go criteria
- **Evidence Integration** — References uploaded operational data
- **Retry & Fallback** — Graceful degradation on LLM failures

## Usage

```bash
curl -X POST http://localhost:8000/api/workspace/operations \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "We need to automate 40 warehouse facilities across 24 countries within 18 months while maintaining current throughput levels."
  }'
```

### Response Structure

```json
{
  "agent_id": "operations",
  "position": "conditional",
  "confidence": 0.60,
  "domain_assessment": {
    "execution_complexity": "high",
    "timeline_estimate": "22-28 months realistically (buffer for international logistics)",
    "resource_requirements": "12 dedicated engineers + 3 regional project managers + vendor partnerships",
    "capacity_impact": "overload",
    "dependencies": ["IT infrastructure readiness", "Local regulatory approvals", "Vendor procurement"]
  },
  "implementation_phases": [
    "Phase 1 — Pilot (Months 1-4): 3 facilities in primary market",
    "Phase 2 — Regional rollout (Months 5-16): 20 facilities across 3 regions",
    "Phase 3 — Global completion (Months 17-28): Remaining 17 facilities"
  ]
}
```

## Project Structure

```
operations/
├── __init__.py       # Package exports
├── prompt.py         # COO system prompt
├── schema.py         # Pydantic models (complexity, capacity enums)
├── service.py        # Agent service with retry logic
└── examples.py       # Few-shot examples
```

## Future Enhancements

- Integration with project management tools (Jira, Asana)
- Resource availability calendar integration
- Supply chain simulation modeling
- Automated Gantt chart generation from phase plans
- Historical execution variance tracking

## License

MIT License
