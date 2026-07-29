# Consensus Engine Specification

## Overview

The Consensus Engine is the synthesis core of the AI Boardroom. It receives structured agent positions after the final deliberation round, detects agreement and disagreement patterns, scores positions using a weighted algorithm, and produces a unified recommendation that preserves both majority consensus and minority dissent.

## Responsibilities

1. Receive all final-round agent positions from the Orchestrator
2. Score individual positions using the consensus algorithm
3. Detect agreement levels across agents
4. Identify key points of contention and unresolved disagreements
5. Synthesize a unified recommendation from multi-agent outputs
6. Preserve dissenting views for transparency
7. Return structured synthesis results to the Orchestrator

## Relationship to Other Components

| Component | Relationship |
|-----------|-------------|
| Orchestrator | Invoked by Orchestrator after Round 3 is complete; returns synthesis results |
| Department Agents | Consumes their structured outputs; never communicates with agents directly |
| Report Generator | Synthesis results are passed to Report Generator by the Orchestrator |
| Board Context | Reads accumulated deliberation data; writes synthesis results |

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Final agent positions | Orchestrator | All Round 3 structured responses from participating agents |
| Deliberation history | Board Context | Full history of all rounds (for position-shift detection) |
| Session configuration | Orchestrator | Participating agents, weighting rules, consensus threshold |

## Outputs

| Output | Description |
|--------|-------------|
| Consensus score | Numerical score (0.0–1.0) representing overall agreement level |
| Consensus level | Classification: strong, moderate, split, or no consensus |
| Unified recommendation | Synthesized position integrating majority perspectives |
| Executive summary | One-paragraph recommendation narrative |
| Key agreements | Points where agents converge |
| Key disagreements | Points of unresolved contention with reasoning |
| Dissenting views | Minority positions preserved with rationale |
| Risk matrix | Aggregated risks by domain and severity |
| Conditions | Shared preconditions identified across multiple agents |
| Recommended next steps | Actionable follow-up items |

## Consensus Algorithm

### Position Scoring

Each agent's final position is mapped to a numerical value:

| Position | Score Formula |
|----------|--------------|
| Support | +1.0 × confidence |
| Conditional | +0.5 × confidence |
| Neutral | 0.0 |
| Oppose | −1.0 × confidence |

### Weighted Scoring

When a scenario falls within a specific domain, the relevant agent receives a weight boost:

| Scenario Domain | Boosted Agent(s) | Weight Multiplier |
|-----------------|------------------|-------------------|
| Financial decisions | Finance | ×1.5 |
| Technical decisions | IT | ×1.5 |
| People/org decisions | HR | ×1.5 |
| Market decisions | Marketing, Sales | ×1.25 each |
| Legal/compliance | Legal | ×1.5 |
| Operational decisions | Operations | ×1.5 |
| Data/measurement | Business Analytics | ×1.5 |

Domain classification is determined by the Orchestrator when dispatching the session.

### Consensus Levels

| Level | Threshold | Behavior |
|-------|-----------|----------|
| Strong Consensus | ≥ 75% weighted agreement | Clear recommendation with high confidence |
| Moderate Consensus | 50–74% | Recommendation with noted dissent |
| Split Decision | 25–49% | Balanced presentation of competing positions |
| No Consensus | < 25% | Multiple viable paths presented; no single recommendation |

## Synthesis Behavior

The synthesis module produces a structured output that includes:

1. **Executive Summary** — One-paragraph recommendation based on the consensus level
2. **Consensus Score** — Numerical score with agent-by-agent breakdown
3. **Key Arguments For** — Strongest supporting rationales across agents
4. **Key Arguments Against** — Strongest opposing rationales across agents
5. **Shared Conditions** — Conditions that appear across 3+ agents
6. **Risk Matrix** — All risks aggregated, deduplicated, and categorized by domain and severity
7. **Dissenting Views** — Each minority position with its full rationale preserved
8. **Recommended Next Steps** — Actionable items prioritized by consensus strength

## Session State Lifecycle

```
ROUND_3_COMPLETE → SYNTHESIZING → SYNTHESIS_COMPLETE
```

The Consensus Engine is invoked only after Round 3 is complete. It does not participate in earlier rounds.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Fewer than minimum required agents | Proceed with available agents; note reduced confidence |
| Agent response fails schema validation | Exclude from scoring; note absence |
| Tie in consensus scoring | Present as split decision with both paths |
| All agents oppose | Produce "Do not proceed" recommendation with rationale |
| All agents support | Produce strong recommendation; note absence of challenge |

## Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Minimum agents for consensus | Fewest agents required to produce a valid synthesis | 5 |
| Consensus threshold | Score required for "strong consensus" | 0.75 |
| Enable weighted scoring | Whether domain-specific weighting is applied | Yes |
| Preserve dissent threshold | Minimum confidence for a dissenting view to be preserved | 0.5 |

## Design Constraints

- Must never make its own business judgment — it aggregates and synthesizes agent positions only
- Must preserve all dissenting views above the confidence threshold — consensus does not mean unanimity
- Must produce the same synthesis result given the same inputs (deterministic scoring)
- Must not communicate with agents directly — all input comes via the Orchestrator
- Must handle partial data gracefully (missing agents, incomplete responses)
- Must operate only on structured data (the shared output schema) — never on raw LLM text

## Success Criteria

- Consensus scores are mathematically reproducible from agent positions
- Synthesis clearly reflects the balance of perspectives (not just majority opinion)
- Dissenting views are preserved with their original rationale
- Risk matrix covers all domains represented by participating agents
- Recommended next steps are actionable and traceable to specific agent inputs
- Executive summary accurately reflects the consensus level (not over-confident on split decisions)
