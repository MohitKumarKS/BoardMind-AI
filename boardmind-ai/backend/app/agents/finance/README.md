# Finance AI Agent (CFO)

An AI-powered Chief Financial Officer agent that provides quantified financial analysis, ROI projections, risk-adjusted return assessments, and capital allocation recommendations for business proposals.

## Project Overview

The Finance AI Agent embodies the mindset of a conservative, numbers-first CFO. It evaluates business proposals exclusively through the lens of financial strategy — analyzing revenue impact, cost structures, ROI projections, payback periods, and financial risk exposure. Every claim is backed by quantification, and every recommendation includes measurable thresholds.

## Problem Statement

Financial analysis of business proposals often suffers from:
- **Qualitative hand-waving** — vague claims about "significant ROI" without quantification
- **Missing assumptions** — projections presented without stating what must be true for them to hold
- **Siloed analysis** — finance teams analyze in isolation without structured output for cross-functional review
- **Slow turnaround** — days or weeks to produce a CFO-level financial assessment

## Solution

The Finance AI Agent delivers:
- Instant, structured financial analysis with explicit quantification
- Revenue impact, cost impact, ROI, and payback period estimates
- Financial risk classification (low/medium/high) with specific exposure scenarios
- Measurable conditions that must be met for financial support
- KPI recommendations for ongoing monitoring
- Evidence-aware analysis when financial data is uploaded via MCP

## Agent Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Revenue Impact | Projected revenue change with timeline and assumptions |
| Cost Analysis | Total cost including hidden costs, ongoing operational burden |
| ROI Estimation | Projected return on investment with clearly stated assumptions |
| Payback Period | Time to recoup initial investment under various scenarios |
| Risk Classification | Overall financial risk level with quantified exposure |
| KPI Recommendations | Specific financial metrics to monitor post-decision |

## Features

- **Quantified Analysis** — Every financial claim includes numbers or ranges
- **Explicit Assumptions** — All projections state what must be true
- **Risk-Adjusted Returns** — Downside scenarios alongside best-case projections
- **Evidence Integration** — References uploaded financial data (revenue forecasts, budgets, P&L)
- **Retry & Fallback** — Graceful recovery from LLM failures with mock response
- **Response Normalization** — Handles malformed LLM output (wrong types, missing fields)
- **Position Independence** — Takes genuine stance (support/oppose/conditional/neutral) based on financial merits

## Architecture

```
FinanceAgentRequest (scenario + context)
         │
         ▼
┌─────────────────────┐
│  build_finance_prompt │ ── Combines scenario + evidence + instructions
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  retry_llm_call()    │ ── 2 retries + mock fallback
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  _parse_and_validate │ ── JSON parse → normalize → Pydantic validate
└──────────┬──────────┘
           │
           ▼
    FinanceAgentResponse
```

### Key Components

- `prompt.py` — System prompt establishing CFO persona + JSON schema
- `schema.py` — Pydantic models for request/response validation
- `service.py` — Orchestrates LLM call, parsing, validation, and mock fallback
- `examples.py` — Few-shot examples for prompt engineering

## Technology Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq (Llama 3.1 8B / 3.3 70B) |
| Validation | Pydantic v2 with field validators |
| Retry Logic | Custom async retry with exponential backoff |
| Framework | FastAPI (async endpoint) |
| Evidence | MCP file upload + structured extraction |

## Installation & Setup

This agent runs as part of the BoardMind AI backend:

```bash
cd boardmind-ai/backend
pip install -r requirements.txt

# Set your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

### Standalone (Department Workspace Mode)

```bash
curl -X POST http://localhost:8000/api/workspace/finance \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "We are considering investing $5M in a new AI product targeting enterprise customers with a 12-month development timeline.",
    "context": "Current annual revenue: $50M. Available capital: $12M."
  }'
```

### As Part of Boardroom (Orchestrated Mode)

The Finance Agent is automatically invoked by the Executive Orchestrator when the Decision Router determines financial analysis is relevant to the scenario.

### Response Structure

```json
{
  "agent_id": "finance",
  "position": "conditional",
  "confidence": 0.72,
  "domain_assessment": {
    "revenue_impact": "Projected +$8M ARR by Year 2, assuming 5% market penetration",
    "cost_impact": "Initial $5M + $1.2M/year operational. Hidden: $800K integration costs",
    "roi_estimate": "Expected 160% ROI over 3 years, assuming 15% YoY growth",
    "payback_period": "18-22 months at projected adoption rates",
    "risk_level": "medium"
  },
  "summary": "The financial case is promising but requires validation of revenue assumptions before full commitment.",
  "rationale": "...",
  "risks": ["Revenue projections rely on unvalidated market assumptions"],
  "conditions": ["Validate CAC < $5K with pilot data before Phase 2 funding"],
  "metrics_to_track": ["Monthly burn rate vs. plan", "CAC/LTV ratio"]
}
```

## Project Structure

```
finance/
├── __init__.py       # Package exports
├── prompt.py         # CFO system prompt + user prompt builder
├── schema.py         # Pydantic request/response models
├── service.py        # Agent service (LLM invocation + validation)
└── examples.py       # Few-shot examples for prompt quality
```

## Future Enhancements

- Multi-round deliberation with position refinement based on other agents' input
- Integration with real financial APIs (QuickBooks, SAP, Xero)
- Monte Carlo simulation for risk quantification
- Sensitivity analysis with automated parameter sweeps
- Historical decision outcome tracking for confidence calibration

## License

MIT License
