# Orchestrator Specification

## Overview

The Orchestrator is the workflow coordinator for the AI Boardroom's Executive Boardroom mode. It receives user business requests, determines which agents participate, manages deliberation rounds, publishes outputs to the Board Context, invokes the Consensus Engine, and triggers the Report Generator. The Orchestrator never makes business decisions itself.

## Core Principle

The Orchestrator is NOT a department agent. It has no business opinion, no domain expertise, and no position on any scenario. Its sole responsibility is ensuring that the right agents are engaged, rounds proceed in order, and outputs flow to the correct downstream components.

## Responsibilities

1. Receive the user's business request from the API Gateway
2. Classify the scenario domain to determine weighting (for Consensus Engine)
3. Determine which department agents should participate (default: all 8)
4. Initialize the deliberation session and Board Context
5. Dispatch Round 1 prompts to all participating agents (independent analysis)
6. Collect and validate Round 1 responses; publish to Board Context
7. Dispatch Round 2 prompts with Round 1 context (debate and challenge)
8. Collect and validate Round 2 responses; publish to Board Context
9. Dispatch Round 3 prompts with Round 2 context (final positions)
10. Collect and validate Round 3 responses; publish to Board Context
11. Invoke the Consensus Engine with all final positions and session configuration
12. Receive synthesis results from Consensus Engine
13. Trigger the Report Generator with synthesis results and deliberation history
14. Emit events to the UI throughout the process via the event stream
15. Handle errors, timeouts, and partial failures gracefully

## Relationship to Other Components

| Component | Relationship |
|-----------|-------------|
| API Gateway | Receives user requests from; sends final results back to |
| Department Agents | Dispatches prompts to; collects structured responses from |
| Consensus Engine | Invokes after Round 3; receives synthesis results from |
| Report Generator | Triggers with synthesis + history; receives report reference from |
| Board Context | Writes all session data to; provides read context to agents |
| Boardroom UI | Emits real-time events to (via event stream) |

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Business scenario | API Gateway | User's question, proposal, or decision to evaluate |
| Session configuration | API Gateway / defaults | Agent selection, urgency level, custom parameters |

## Outputs

| Output | Destination | Description |
|--------|-------------|-------------|
| Round prompts | Department Agents | Scenario + accumulated context for each round |
| Session events | Boardroom UI (via event stream) | Real-time status updates |
| Board Context updates | Board Context | All agent responses, organized by round |
| Synthesis request | Consensus Engine | Final positions + session config |
| Report request | Report Generator | Synthesis results + full deliberation history |
| Session result | API Gateway | Final report reference + session status |

## Workflow — Executive Boardroom Mode

```
1. Receive scenario from API Gateway
2. Classify scenario domain
3. Select participating agents (default: all 8)
4. Create session in Board Context
5. Emit: session_created

6. Emit: round_started (Round 1)
7. Dispatch scenario to all agents (no cross-agent context)
8. Collect responses (with timeout handling)
9. Validate response schemas
10. Publish Round 1 responses to Board Context
11. Emit: round_complete (Round 1)

12. Emit: round_started (Round 2)
13. Dispatch scenario + all Round 1 positions to all agents
14. Collect responses (with timeout handling)
15. Validate response schemas
16. Publish Round 2 responses to Board Context
17. Emit: round_complete (Round 2)

18. Emit: round_started (Round 3)
19. Dispatch scenario + Round 1 + Round 2 positions to all agents
20. Collect responses (with timeout handling)
21. Validate response schemas
22. Publish Round 3 responses to Board Context
23. Emit: round_complete (Round 3)

24. Emit: consensus_started
25. Invoke Consensus Engine with final positions + config
26. Receive synthesis results
27. Publish synthesis to Board Context
28. Emit: consensus_complete

29. Trigger Report Generator with synthesis + full history
30. Receive report reference
31. Emit: report_ready
32. Emit: session_complete
33. Return result to API Gateway
```

## Agent Selection Logic

By default, all 8 department agents participate. The Orchestrator may exclude agents when:

| Condition | Behavior |
|-----------|----------|
| User explicitly deselects agents | Respect user preference |
| Scenario is clearly single-domain | Include all agents (broader perspective is the product value) |
| An agent fails during Round 1 | Continue without it; note absence |

The Orchestrator should bias toward inclusion. Excluding agents reduces the value of multi-perspective analysis.

## Scenario Domain Classification

The Orchestrator classifies each scenario into one or more domains to inform the Consensus Engine's weighted scoring:

| Domain | Indicators |
|--------|-----------|
| Financial | Revenue, cost, budget, investment, pricing, margin |
| Technical | Systems, architecture, security, infrastructure, platform |
| People/Org | Hiring, culture, team, compensation, organizational change |
| Market | Customers, competition, positioning, launch, brand |
| Legal/Compliance | Regulation, contracts, liability, privacy, governance |
| Operational | Process, capacity, timeline, delivery, execution |
| Data/Measurement | Metrics, analytics, measurement, evidence, tracking |

Multiple domains may apply. Classification does not exclude agents — it adjusts weighting only.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Agent timeout (30s) | Use partial response if available; proceed without agent if not; note in Board Context |
| Agent response fails schema validation | Request one retry; if still invalid, exclude and note |
| Agent produces empty response | Exclude from round; note in Board Context |
| Multiple agents fail | Continue if ≥5 agents remain; abort if <5 |
| Consensus Engine failure | Retry once; if still fails, return error to user with raw positions |
| Report Generator failure | Return synthesis results without formatted report; offer retry |

## Event Emission

The Orchestrator is responsible for emitting all lifecycle events to the UI event stream. Events must be emitted in real-time as state transitions occur — not batched at the end.

## Design Constraints

- Must NEVER express a business opinion, take a position, or influence agent outputs
- Must NEVER modify, filter, or summarize agent responses before publishing to Board Context
- Must dispatch to all selected agents in parallel within each round (not sequentially)
- Must not proceed to the next round until all agents have responded (or timed out)
- Must preserve complete agent responses in the Board Context (no truncation or summarization)
- Must be stateless between sessions — each deliberation is independent
- Must emit events in real-time for UI responsiveness
- Must handle partial failures without abandoning the entire session

## Success Criteria

- Deliberation completes end-to-end (scenario → report) within 2 minutes for standard scenarios
- All participating agents receive the correct context for each round
- Board Context contains complete, unmodified agent responses after each round
- Events are emitted in real-time (within 200ms of state transition)
- Error handling preserves maximum deliberation value (graceful degradation, not hard failure)
- The Orchestrator's behavior is fully transparent — no hidden logic that affects outcomes
- No business judgment leaks into orchestration decisions
