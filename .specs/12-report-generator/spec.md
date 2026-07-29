# Report Generator Specification

## Overview

The Report Generator transforms deliberation outcomes into structured, professional executive reports. It assembles agent analyses, consensus results, and synthesis into documents suitable for executive review and decision-making.

## Responsibilities

1. Receive synthesis results and full deliberation history from the Orchestrator
2. Assemble report sections from structured deliberation data
3. Generate narrative content (executive summary) from structured inputs
4. Produce output in multiple formats (Markdown, PDF, HTML)
5. Validate report completeness before delivery
6. Support customization of report scope and verbosity

## Relationship to Other Components

| Component | Relationship |
|-----------|-------------|
| Orchestrator | Invoked by Orchestrator after Consensus Engine completes; receives all data |
| Consensus Engine | Consumes synthesis results (consensus score, recommendation, dissent) |
| Department Agents | Consumes their structured outputs from all rounds (via deliberation history) |
| Boardroom UI | Reports are displayed in the UI Report View and available for download |

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Synthesis results | Consensus Engine (via Orchestrator) | Consensus score, recommendation, agreements, disagreements, dissent |
| Deliberation history | Board Context | All agent responses across all rounds |
| Session metadata | Orchestrator | Session ID, timestamp, scenario text, participating agents |
| Report configuration | User / default | Format, verbosity, section inclusion preferences |

## Outputs

| Output | Description |
|--------|-------------|
| Structured report | Complete report with all sections populated |
| Format variants | Markdown (primary), PDF (professional), HTML (web-shareable) |
| Report metadata | Report ID, generation timestamp, session reference |

## Report Sections

### 1. Executive Summary
- One-paragraph overall recommendation
- Consensus level and confidence
- Critical decision factors (top 3)
- Recommended action in one sentence

### 2. Scenario Context
- Original scenario or question as submitted by the user
- Key assumptions identified during deliberation
- Scope boundaries noted by agents

### 3. Multi-Perspective Analysis
- Each participating agent's final position with summary rationale
- Confidence scores per agent
- Position changes across rounds (with justification for shifts)

### 4. Consensus & Agreement
- Overall consensus score and classification (strong/moderate/split/none)
- Points of agreement across agents (shared conclusions)
- Key areas of disagreement with reasoning from each side
- Minority/dissenting views preserved with full rationale

### 5. Risk Assessment
- Aggregated risk matrix (likelihood × impact)
- Risks categorized by domain (financial, legal, operational, technical, people, market)
- Mitigation strategies suggested by agents
- Unresolved risks flagged for further investigation

### 6. Conditions & Prerequisites
- Shared conditions identified across 3+ agents
- Dependencies identified across departments
- Required approvals or validations before proceeding

### 7. Recommended Next Steps
- Prioritized action items (high/medium/low)
- Owner suggestions by department
- Timeline recommendations
- Success metrics to track (from Business Analytics and Finance agents)

### 8. Appendix
- Full agent responses per round (expandable/collapsible in HTML)
- Deliberation timeline (when each round started/completed)
- Methodology note (how consensus was calculated)
- List of participating agents and their roles

## Output Formats

### Markdown (Primary)
- Structured with headers, tables, and lists
- Suitable for rendering in the Boardroom UI
- Convertible to other formats

### PDF (Professional)
- Clean professional layout
- Table of contents with section links
- Page numbers and headers
- Visual elements for consensus data (gauge, position chart)

### HTML (Shareable)
- Styled report for web viewing
- Interactive elements (expandable appendix sections)
- Shareable via URL without requiring platform access

## Report Generation Pipeline

1. **Data Collection** — Gather all required inputs (synthesis, history, metadata)
2. **Aggregation** — Compute derived data (risk matrix, agreement points, position shifts)
3. **Narrative Generation** — Generate executive summary and connecting narrative from structured data
4. **Section Assembly** — Populate each report section with computed data and narrative
5. **Format Conversion** — Produce output in requested format(s)
6. **Validation** — Confirm all sections are populated; flag any missing data

## Customization Options

| Option | Values | Default |
|--------|--------|---------|
| Verbosity | Executive brief / Standard / Detailed | Standard |
| Sections included | Any subset of the 8 sections | All |
| Agent filter | Specific agents only | All participating |
| Format | Markdown / PDF / HTML | Markdown |

## Design Constraints

- Must produce reports from structured data only — never from raw LLM conversation text
- Must complete report generation within 10 seconds after receiving synthesis results
- Must handle partial data gracefully (if an agent was excluded, report notes absence)
- Must preserve agent attribution — every insight in the report is traceable to a specific agent
- Must not add recommendations beyond what agents and the Consensus Engine produced
- Must support regeneration with different options without re-running the deliberation
- Reports must be cacheable and retrievable by session ID after generation

## Success Criteria

- Every report section is populated with scenario-specific content (no placeholder text)
- Executive summary accurately reflects the consensus level and recommendation
- Risk matrix covers all domains represented by participating agents
- Position shifts are documented with the agent's stated justification
- Reports are readable and actionable by someone who did not observe the live deliberation
- All three output formats (Markdown, PDF, HTML) contain identical substantive content
