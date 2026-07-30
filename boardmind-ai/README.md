# BoardMind AI - Multi-Agent Executive Boardroom

A multi-agent AI platform that simulates a corporate executive boardroom, where specialized department agents collaboratively analyze business proposals through structured deliberation, consensus building, and executive reporting.

## Project Overview

BoardMind AI replicates the decision-making dynamics of a real corporate board meeting. When a business scenario is submitted, a Decision Router classifies it, selects relevant department agents, and an Executive Orchestrator coordinates their parallel execution. Each agent provides domain-specific analysis, and a Consensus Engine synthesizes their perspectives into a unified executive recommendation.

## Problem Statement

Enterprise decision-making suffers from:
- **Information silos** — departments analyze proposals in isolation without cross-functional visibility
- **Slow deliberation cycles** — weeks of meetings to gather perspectives from Finance, Legal, HR, IT, Operations, Marketing, and Sales
- **Cognitive bias** — individual executives may default to their domain's comfort zone
- **Lack of structured evidence** — decisions often lack quantified risk assessment and measurable conditions

## Solution

BoardMind AI provides:
- **8 specialized AI agents** (CFO, CTO, COO, CHRO, CMO, CRO, General Counsel, CDO) that analyze proposals from their domain expertise
- **Parallel execution** with wave-based scheduling to respect API rate limits
- **Deterministic consensus engine** that detects conflicts, aggregates risks, and produces actionable recommendations
- **MCP data integration** — upload spreadsheets, documents, and files that agents reference in their analysis
- **Executive PDF reports** with full audit trail
- **Session history** with PostgreSQL persistence via MCP Knowledge Hub

## Multi-Agent Workflow

```
User Scenario
     │
     ▼
┌─────────────────┐
│ Decision Router  │ ── ML classification + keyword expansion
└────────┬────────┘
         │ selects agents
         ▼
┌─────────────────┐
│   Orchestrator   │ ── Wave-based parallel execution
└────────┬────────┘
         │ coordinates
         ▼
┌─────────────────────────────────────────────┐
│  Agent Wave 1: Finance, Marketing, Sales, HR │
│  Agent Wave 2: Operations, Legal, IT, CDO    │
└────────┬────────────────────────────────────┘
         │ all complete
         ▼
┌─────────────────┐
│ Board Context    │ ── Shared session state
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Consensus Engine  │ ── Deterministic rules over positions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Report Generator │ ── JSON + PDF output
└─────────────────┘
```

## Features

- **Executive Boardroom Mode** — Full multi-agent orchestration with consensus
- **Department Workspace Mode** — Individual agent analysis for focused questions
- **MCP File Upload** — CSV, Excel, PDF, DOCX ingestion with structured evidence extraction
- **Real-time Execution Timeline** — Visual progress of agent deliberation
- **Consensus Visualization** — Charts showing position distribution and conflicts
- **PDF Executive Reports** — Professional reports with all findings
- **Session History** — PostgreSQL-backed meeting archive with search
- **Retry & Fallback** — Graceful degradation when LLM calls fail
- **Per-Agent Timeout** — No single agent can block the entire session
- **Session Eviction** — Bounded memory usage with LRU eviction

## Architecture

### Backend (Python FastAPI)
- **Decision Router** — scikit-learn classifier + keyword-based agent expansion
- **Executive Orchestrator** — asyncio-based wave scheduling with rate limit detection
- **8 Department Agents** — Each with domain-specific prompts, schemas, and services
- **Consensus Engine** — Deterministic position counting, conflict detection, risk aggregation
- **Board Context** — In-memory session store with asyncio.Lock concurrency control
- **Report Generator** — fpdf2-based PDF generation
- **MCP Integration** — File upload, spreadsheet parsing, evidence summarization
- **Knowledge Hub** — PostgreSQL persistence via SQLAlchemy async

### Frontend (React + TypeScript)
- **Boardroom Page** — Scenario input, agent cards, consensus visualization
- **Workspace Pages** — Per-agent analysis with evidence upload
- **Session History** — Browse and search past meetings
- **Report Download** — PDF generation and download

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | FastAPI 0.115 |
| LLM Provider | Groq (Llama 3.1 8B / 3.3 70B) |
| ML Classification | scikit-learn |
| Database | PostgreSQL + SQLAlchemy async |
| PDF Generation | fpdf2 |
| Data Processing | pandas, openpyxl |
| Frontend Framework | React 18 + TypeScript |
| Build Tool | Vite 5 |
| Routing | React Router 6 |
| Charts | Recharts |
| Animations | Framer Motion |

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (optional, for session history)
- Groq API key (free at console.groq.com)

### Backend Setup

```bash
cd boardmind-ai/backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd boardmind-ai/frontend
npm install
npm run dev
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Groq API key for LLM access |
| `MCP_DATABASE_URL` | No | PostgreSQL connection string for history |
| `LLM_PROVIDER` | No | Force provider: `groq`, `openai`, or `mock` |
| `GROQ_MODEL` | No | Override model (default: llama-3.1-8b-instant) |
| `LLM_MAX_CONCURRENT` | No | Max concurrent LLM calls (default: 2) |

## Usage

1. Open `http://localhost:5173` in your browser
2. Navigate to **Executive Boardroom**
3. Enter a business scenario (optionally upload supporting data)
4. Click **Convene Board** to start multi-agent analysis
5. View department perspectives, consensus, and download the report

## Project Structure

```
boardmind-ai/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── finance/          # CFO agent
│   │   │   ├── marketing/        # CMO agent
│   │   │   ├── sales/            # CRO agent
│   │   │   ├── hr/               # CHRO agent
│   │   │   ├── operations/       # COO agent
│   │   │   ├── legal/            # General Counsel agent
│   │   │   ├── it/               # CTO agent
│   │   │   ├── business_analytics/ # CDO agent
│   │   │   ├── llm_provider.py   # LLM abstraction (Groq/OpenAI/Mock)
│   │   │   ├── retry.py          # Shared retry + fallback logic
│   │   │   ├── response_normalizer.py  # LLM output normalization
│   │   │   ├── evidence.py       # MCP evidence injection
│   │   │   └── evidence_extractor.py   # Data fact extraction
│   │   ├── orchestrator/         # Executive Orchestrator
│   │   ├── consensus/            # Consensus Engine
│   │   ├── board_context/        # Shared session state
│   │   ├── decision_router/      # ML-based scenario routing
│   │   ├── reports/              # PDF report generation
│   │   ├── mcp/                  # MCP file processing tools
│   │   ├── mcp_hub/              # PostgreSQL persistence
│   │   ├── routes/               # FastAPI route handlers
│   │   └── main.py               # Application entry point
│   ├── tests/                    # Adversarial test suite (85 tests)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/boardroom/ # Boardroom UI components
│   │   ├── pages/                # Route pages
│   │   ├── services/             # API client services
│   │   └── types/                # TypeScript interfaces
│   └── package.json
└── README.md
```

## Future Enhancements

- Multi-round deliberation with cross-agent referencing
- Real-time WebSocket streaming of agent responses
- Custom agent persona configuration
- Integration with enterprise data sources (Salesforce, SAP, etc.)
- Role-based access control for different executive levels
- Historical trend analysis across past decisions
- Agent confidence calibration based on outcome tracking

## License

MIT License
