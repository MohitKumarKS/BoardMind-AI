# CEO Agent

## Role
**CEO** — Chief Executive Officer

## Department Objective
Provide strategic vision, corporate direction, stakeholder alignment, and executive prioritization for enterprise decision-making.

## Domain Expertise
- Strategic vision and corporate direction setting
- Stakeholder alignment and executive communication
- Executive prioritization and resource allocation
- Competitive positioning and market leadership
- Cross-functional initiative coordination

## Decision Boundaries

### In Scope
- Strategic vision and long-term corporate direction
- Stakeholder alignment and executive prioritization
- Competitive positioning and market leadership decisions
- Cross-functional initiative approval and coordination
- Corporate culture and organizational direction

### Out of Scope
- Financial modeling and detailed financial analysis (refer to CFO)
- Technology architecture and implementation (refer to CTO)
- Legal and regulatory specifics (refer to GC)

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
  "agent_id": "ceo",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "strategic_alignment": "Assessment of alignment with corporate strategy",
    "stakeholder_impact": "Impact on key stakeholders",
    "competitive_positioning": "Effect on market position",
    "execution_priority": "Priority level for execution",
    "risk_level": "low | medium | high"
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
| strategic_alignment | str | Assessment of alignment with corporate strategy |
| stakeholder_impact | str | Impact on key stakeholders |
| competitive_positioning | str | Effect on competitive market position |
| execution_priority | str | Priority level for execution |
| risk_level | str (low/medium/high) | Overall risk level assessment |

## Usage
```python
from app.agents.ceo import CEOService, CEORequest

service = CEOService()
request = CEORequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
