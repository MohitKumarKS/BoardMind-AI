# Legal AI Agent (General Counsel)

An AI-powered General Counsel agent that evaluates compliance status, legal risk, liability exposure, regulatory requirements, and intellectual property implications of business proposals.

## Project Overview

The Legal AI Agent embodies a cautious yet enabling General Counsel who identifies the compliance pathway rather than simply saying "no." It evaluates proposals through regulatory frameworks, contractual obligations, data privacy requirements, and IP protections.

## Problem Statement

Legal assessment of business initiatives often suffers from:
- **Binary thinking** — Legal says "yes" or "no" without providing a viable path forward
- **Late-stage involvement** — Legal review happens after commitments are made
- **Jurisdiction blindness** — international implications not considered early enough
- **IP exposure** — proprietary information sharing without adequate protections

## Solution

The Legal AI Agent delivers:
- Compliance status assessment (compliant / non-compliant / requires review)
- Legal risk classification (low / medium / high / critical)
- Liability exposure quantification with scenario analysis
- Regulatory body identification for applicable jurisdictions
- IP implications assessment (none / minor / significant)
- Required safeguards that must be in place before proceeding

## Agent Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Compliance Status | Whether the proposal meets regulatory requirements |
| Risk Classification | Overall legal risk level |
| Liability Exposure | Potential financial liability with range estimates |
| Regulatory Bodies | Which regulators and frameworks apply |
| IP Implications | Effect on intellectual property posture |
| Required Safeguards | Legal protections needed before proceeding |

## Features

- **Enabling Posture** — Finds the path to compliance, not just risks
- **Multi-Jurisdiction** — Considers GDPR, CCPA, PCI DSS, and sector-specific rules
- **IP Awareness** — Evaluates patent, copyright, and trade secret implications
- **Contractual Focus** — Identifies needed agreements and protections
- **Evidence Integration** — References uploaded legal documents and policies
- **Retry & Fallback** — Graceful degradation on LLM failures

## Usage

```bash
curl -X POST http://localhost:8000/api/workspace/legal \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "We plan to expand into 5 new international markets with AI-powered customer profiling and cross-border data transfers."
  }'
```

### Response Structure

```json
{
  "agent_id": "legal",
  "position": "conditional",
  "confidence": 0.70,
  "domain_assessment": {
    "compliance_status": "requires_review",
    "risk_level": "high",
    "liability_exposure": "Potential $2-10M exposure from GDPR violations",
    "regulatory_bodies": ["GDPR (EU)", "CCPA (California)", "Local DPAs"],
    "ip_implications": "minor"
  },
  "required_safeguards": [
    "Data processing agreements for all cross-border transfers",
    "Privacy impact assessment for AI profiling activities",
    "Regulatory counsel engagement in each target jurisdiction"
  ]
}
```

## Project Structure

```
legal/
├── __init__.py       # Package exports
├── prompt.py         # General Counsel system prompt
├── schema.py         # Pydantic models (compliance, risk, IP enums)
├── service.py        # Agent service with retry logic
└── examples.py       # Few-shot examples
```

## Future Enhancements

- Integration with legal research APIs (Westlaw, LexisNexis)
- Automated contract clause generation for identified risks
- Regulatory change monitoring and alerting
- Jurisdiction-specific compliance checklist generation
- Historical regulatory enforcement data integration

## License

MIT License
