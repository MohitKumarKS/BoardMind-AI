# System Architecture Specification

## Overview

The AI Boardroom system follows a multi-agent orchestration architecture where specialized department agents communicate through a central Orchestrator and Consensus Engine. The system is event-driven, enabling real-time streaming of deliberation to the frontend.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Boardroom UI                             │
│            Real-time deliberation visualization               │
└──────────────────────────┬──────────────────────────────────┘
                           │ WebSocket + REST
┌──────────────────────────▼──────────────────────────────────┐
│                       API Gateway                             │
│         Session management, input validation, auth            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                       Orchestrator                            │
│    Request routing │ Agent selection │ Round coordination     │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Department │  │   Consensus  │  │    Report    │
│    Agents    │  │    Engine    │  │   Generator  │
│  (8 agents)  │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Component Responsibilities

### API Gateway

- Expose REST endpoints for session management, scenario submission, and report retrieval
- Maintain WebSocket connections for real-time deliberation streaming
- Authenticate and authorize user sessions
- Validate and sanitize all inputs
- Rate-limit requests to prevent abuse

### Orchestrator

- Receive business scenarios from the API Gateway
- Determine which department agents should participate
- Coordinate deliberation rounds (dispatch, collect, advance)
- Publish outputs to the Board Context (shared state)
- Invoke the Consensus Engine after final round
- Trigger the Report Generator with synthesis results
- Never make business decisions — coordination only

### Department Agents (×8)

- Receive scenario and round context from the Orchestrator
- Produce structured responses conforming to the shared output schema
- Maintain position consistency across rounds (shifts require justification)
- Operate identically in Department Workspace (solo) and Executive Boardroom (multi-agent) modes

### Consensus Engine

- Receive all final-round agent positions
- Score positions using weighted consensus algorithm
- Detect agreement levels (strong consensus, moderate, split, no consensus)
- Synthesize a unified recommendation from multi-agent outputs
- Preserve dissenting views and unresolved disagreements

### Report Generator

- Receive synthesis results and full deliberation history
- Assemble structured executive report with defined sections
- Support multiple output formats (Markdown, PDF, HTML)
- Generate executive summary narrative from structured data

### Boardroom UI

- Display real-time agent deliberation via WebSocket streaming
- Visualize consensus formation and position shifts
- Provide scenario input and session management
- Show agent detail panels and report output

## Operational Modes

### Department Workspace Mode

```
User → API Gateway → Single Agent → Response to User
```

- No Orchestrator involvement
- No Consensus Engine
- No Report Generator
- Direct single-agent interaction for focused analysis

### Executive Boardroom Mode

```
User → API Gateway → Orchestrator → Agents (Round 1)
                                   → Agents (Round 2)
                                   → Agents (Round 3)
                                   → Consensus Engine
                                   → Report Generator → User
```

- Full multi-round deliberation
- All system components active
- Real-time streaming to UI throughout

## Data Flow — Executive Boardroom

1. User submits a business scenario via UI or API
2. API Gateway validates input and creates a deliberation session
3. Orchestrator receives scenario and selects participating agents
4. **Round 1 — Independent Analysis**: Each agent receives the scenario; no cross-agent visibility; produces initial position
5. **Round 2 — Debate & Challenge**: Agents receive all Round 1 positions; respond to others; refine own position
6. **Round 3 — Final Position**: Agents receive Round 2 debate; submit final position and confidence score
7. Orchestrator invokes Consensus Engine with all final positions
8. Consensus Engine scores, synthesizes, and produces unified recommendation
9. Orchestrator triggers Report Generator with synthesis + deliberation history
10. Report delivered to user; session marked complete

## Shared Communication Schema

All agents produce responses conforming to this structure:

```
agent_id          — Unique identifier for the department
round             — Current deliberation round (1, 2, or 3)
position          — support | oppose | neutral | conditional
confidence        — 0.0 to 1.0
domain_assessment — Agent-specific structured analysis
summary           — One-sentence position statement
rationale         — Detailed reasoning (2-4 paragraphs)
risks             — List of domain-specific risks identified
conditions        — Requirements for support
references_to     — Other agent_ids referenced in reasoning
```

## Board Context (Shared State)

The Board Context is the shared data store that accumulates during deliberation:

- Original scenario text
- Session metadata (ID, timestamp, participating agents)
- All agent responses organized by round
- Consensus scores and synthesis results
- Report output reference

All agents read from the Board Context (via Orchestrator-provided round context) but do not write to it directly. Only the Orchestrator publishes to the Board Context.

## Event Stream

Events are published to the UI via WebSocket throughout deliberation:

| Event | Trigger |
|-------|---------|
| `session_created` | New deliberation session initialized |
| `round_started` | Orchestrator begins a new round |
| `agent_thinking` | Agent has received prompt, generating response |
| `agent_response_chunk` | Streaming token from an agent |
| `agent_response_complete` | Agent has finished responding |
| `round_complete` | All agents have responded for current round |
| `consensus_started` | Consensus Engine begins synthesis |
| `consensus_complete` | Synthesis result available |
| `report_ready` | Final report generated and available |
| `session_complete` | Full deliberation lifecycle complete |
| `error` | Any component failure or timeout |

## Non-Functional Requirements

- **Latency**: Agent responses begin streaming within 2 seconds of dispatch
- **Throughput**: Support multiple concurrent deliberation sessions
- **Resilience**: If an agent fails, deliberation continues with remaining agents; absence noted in report
- **Timeout**: Individual agent timeout of 30 seconds; partial results used if timeout occurs
- **Observability**: Structured logging of all orchestration steps, agent dispatches, and consensus computations
- **Security**: Input sanitization, no PII in agent prompts, rate limiting on API endpoints
- **Idempotency**: Sessions can be safely retried without duplicate side effects

## Design Constraints

- The Orchestrator must never make business decisions — it is purely a coordination layer
- Department agents must be stateless between sessions — no cross-session memory
- The same agent definitions must work in both Department Workspace and Executive Boardroom modes
- The Consensus Engine operates only on structured agent outputs, never on raw LLM text
- All inter-component communication uses the shared schema — no component-specific protocols
