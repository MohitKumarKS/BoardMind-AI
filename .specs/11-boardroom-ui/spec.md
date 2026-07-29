# Boardroom UI Specification

## Overview

The Boardroom UI is the user-facing interface for the AI Boardroom platform. It provides real-time visualization of agent deliberations, consensus formation, and report output. It supports both Department Workspace (single-agent) and Executive Boardroom (multi-agent) modes.

## User Experience Modes

### Department Workspace Mode

- User selects a single department agent
- Submits a business scenario or question
- Receives focused, single-perspective analysis in real-time
- No deliberation rounds, no consensus visualization

### Executive Boardroom Mode

- User submits a scenario to the full boardroom
- Observes multi-round deliberation in real-time
- Sees agents form positions, debate, and shift views
- Watches consensus emerge across rounds
- Receives a final synthesized report

## Pages & Views

### 1. Home / Scenario Input

- Text input for business scenario or question
- Mode selector: Department Workspace vs. Executive Boardroom
- Agent selector (Department Workspace mode: choose one; Boardroom mode: all or subset)
- Scenario templates and examples for quick start
- Session history for past deliberations

### 2. Department Workspace View

- Single agent avatar and identity display
- Real-time streaming of agent response
- Structured output display (position, rationale, risks, conditions)
- Option to ask follow-up questions or submit a new scenario

### 3. Executive Boardroom View

- Visual representation of all participating agents (boardroom table metaphor)
- Round indicator showing current deliberation phase (Round 1, 2, or 3)
- Agent status indicators (waiting, thinking, speaking, complete)
- Real-time streaming of agent responses as they generate
- Live consensus meter showing emerging agreement level
- Cross-reference indicators (which agents are responding to whom)

### 4. Agent Detail Panel

- Individual agent's full response for the current round
- Position history across rounds (shows shifts with justification)
- Confidence level visualization
- Risks and conditions highlighted
- References to other agents' positions

### 5. Consensus Dashboard

- Overall consensus score with visual gauge
- Position breakdown by agent (support/oppose/neutral/conditional)
- Key agreement points and disagreement points
- Synthesis summary once available
- Dissenting views section

### 6. Report View

- Full generated report with section navigation
- Download options (PDF, Markdown)
- Expandable sections for detail levels
- Agent attribution for each insight

## Real-Time Event Handling

The UI subscribes to the event stream (WebSocket) and updates reactively:

| Event | UI Behavior |
|-------|-------------|
| `session_created` | Navigate to Boardroom view; show session initialized |
| `round_started` | Update round indicator; reset agent statuses to "waiting" |
| `agent_thinking` | Show thinking animation on agent avatar |
| `agent_response_chunk` | Stream text into agent's response card |
| `agent_response_complete` | Mark agent as complete; show full structured output |
| `round_complete` | Transition round indicator; enable next-round view |
| `consensus_started` | Show synthesis in progress indicator |
| `consensus_complete` | Display consensus score and synthesis |
| `report_ready` | Enable report view navigation |
| `session_complete` | Mark session as complete; show final state |
| `error` | Display contextual error message; offer retry |

## Agent Visual Identity

| Agent | Color | Icon Concept |
|-------|-------|--------------|
| Finance | Green | Chart / Dollar |
| Marketing | Purple | Megaphone |
| Sales | Blue | Handshake |
| HR | Orange | People |
| Operations | Gray | Gear |
| Legal | Red | Scale |
| IT | Teal | Code |
| Business Analytics | Indigo | Graph |

## Visual Design Principles

- **Boardroom metaphor**: Agents arranged in circular/table layout suggesting executive meeting
- **Color coding**: Each agent has a distinct color for instant identification
- **Progressive disclosure**: Summary first; expand for full detail on click
- **Motion with purpose**: Animations signal state transitions (thinking → speaking → done)
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support, sufficient color contrast

## Responsive Design

| Viewport | Layout |
|----------|--------|
| Desktop (≥1024px) | Full boardroom table view with all agents visible simultaneously |
| Tablet (768–1023px) | Condensed layout with scrollable agent cards |
| Mobile (<768px) | Stacked card view with agent selector/carousel |

## Design Constraints

- Must support both operational modes (Department Workspace and Executive Boardroom) with a unified design language
- Must handle streaming responses gracefully — no loading spinners blocking the entire view
- Must remain responsive during active deliberation — UI never freezes waiting for agents
- Must display all agent positions simultaneously during boardroom mode (no hidden agents)
- Must preserve full deliberation history within a session (scrollback to earlier rounds)
- Must be accessible to users with assistive technologies (WCAG 2.1 AA minimum target)

## Success Criteria

- Users can submit a scenario and observe deliberation within 3 clicks from the home page
- Real-time updates appear within 200ms of receiving WebSocket events
- All agent positions are visible without scrolling on desktop in boardroom mode
- Consensus formation is visually clear as it develops (not just a final score)
- Reports are navigable and downloadable directly from the UI
- Mode switching (Department Workspace ↔ Executive Boardroom) is seamless with no page reload
