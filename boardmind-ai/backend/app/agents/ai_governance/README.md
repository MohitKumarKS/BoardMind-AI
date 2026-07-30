# AI Governance Agent

## Role
**AIGO** — AI Governance & Ethics Officer

## Department Objective
Ensure responsible AI deployment, algorithmic fairness, ethical AI practices, and model governance across the organization.

## Domain Expertise
- AI ethics and responsible AI frameworks
- Algorithmic fairness and bias detection
- Model governance and lifecycle management
- AI transparency and explainability
- Societal impact assessment of AI systems

## Decision Boundaries

### In Scope
- Ethical risk assessment of AI initiatives
- Transparency and explainability requirements
- Governance framework compliance
- Societal impact evaluation
- AI risk level classification

### Out of Scope
- AI architecture and model engineering (refer to CTO)
- Data engineering and data pipelines (refer to CDO)
- Legal specifics and regulatory interpretation (refer to GC)
- Cybersecurity of AI systems (refer to CISO)

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
  "agent_id": "ai_governance",
  "position": "support | oppose | neutral | conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "ethical_risk": "Assessment of ethical risks",
    "transparency_requirements": "Transparency and explainability needs",
    "governance_framework": "Applicable governance frameworks",
    "societal_impact": "Broader societal implications",
    "ai_risk_level": "low | medium | high | critical"
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
| ethical_risk | str | Assessment of ethical risks and concerns |
| transparency_requirements | str | Transparency and explainability needs |
| governance_framework | str | Applicable governance frameworks and standards |
| societal_impact | str | Broader societal implications of the initiative |
| ai_risk_level | str (low/medium/high/critical) | Overall AI risk level classification |

## Usage
```python
from app.agents.ai_governance import AIGovernanceService, AIGovernanceRequest

service = AIGovernanceService()
request = AIGovernanceRequest(scenario="Your business proposal here")
response = await service.analyze(request)
```

## Files
- `schema.py` — Pydantic models (Request, Response, DomainAssessment)
- `service.py` — Agent service with LLM invocation and mock fallback
- `prompt.py` — System prompt and prompt builder
- `examples.py` — Example scenarios and expected responses
- `__init__.py` — Public exports
