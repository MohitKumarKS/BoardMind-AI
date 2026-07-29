"""Consensus Engine service.

Analyzes the completed Board Context and produces a single executive
recommendation. No LLM calls — purely deterministic logic over
structured agent responses.

The Consensus Engine:
1. Reads the completed Board Context
2. Reviews every department response (position, confidence, risks)
3. Detects agreement and disagreement
4. Produces one executive recommendation
5. Stores the consensus back into the Board Context
"""

import logging
from typing import Any

from app.board_context import BoardContextService, BoardContext, ConsensusResult

logger = logging.getLogger(__name__)

# Position values normalized to lowercase
SUPPORT = "support"
CONDITIONAL = "conditional"
NEUTRAL = "neutral"
OPPOSE = "oppose"


class ConsensusEngineService:
    """Produces executive recommendations from Board Context.

    Uses deterministic rules over structured agent outputs.
    No LLM, no external calls.

    Usage:
        engine = ConsensusEngineService(board_context_service)
        result = engine.analyze(session_id)
    """

    def __init__(self, board_context: BoardContextService):
        self._board_context = board_context

    def analyze(self, session_id: str) -> ConsensusResult:
        """Run consensus analysis on a completed board session.

        Args:
            session_id: The session to analyze.

        Returns:
            ConsensusResult with decision, conflicts, risks, and actions.

        Raises:
            ValueError: If session not found or not completed.
        """
        context = self._board_context.get_context(session_id)
        if not context:
            raise ValueError(f"Session '{session_id}' not found")

        if context.status not in ("completed", "in_progress"):
            raise ValueError(
                f"Session '{session_id}' has status '{context.status}' — "
                f"consensus requires a completed session"
            )

        # Extract positions from completed agents
        positions = self._extract_positions(context)
        participating_agents = list(positions.keys())

        if not participating_agents:
            raise ValueError(f"No completed agent responses in session '{session_id}'")

        # Count positions
        counts = self._count_positions(positions)

        # Determine decision
        decision, confidence = self._determine_decision(counts, positions)

        # Detect conflicts
        conflict_detected, conflicting_agents = self._detect_conflicts(positions)

        # Aggregate risks and actions
        key_risks = self._aggregate_risks(context)
        recommended_actions = self._aggregate_actions(context)

        # Build executive summary
        executive_summary = self._build_summary(
            decision, counts, conflicting_agents, context
        )

        result = ConsensusResult(
            decision=decision,
            confidence=round(confidence, 3),
            support_count=counts[SUPPORT],
            conditional_count=counts[CONDITIONAL],
            neutral_count=counts[NEUTRAL],
            oppose_count=counts[OPPOSE],
            participating_agents=participating_agents,
            conflict_detected=conflict_detected,
            conflicting_agents=conflicting_agents,
            executive_summary=executive_summary,
            key_risks=key_risks,
            recommended_actions=recommended_actions,
        )

        # Store consensus back into Board Context
        context.consensus_result = result
        context.status = "consensus_complete"

        logger.info(
            f"Consensus for session {session_id}: decision={decision}, "
            f"confidence={confidence:.2f}, conflicts={conflict_detected}"
        )

        return result

    def _extract_positions(
        self, context: BoardContext
    ) -> dict[str, dict[str, Any]]:
        """Extract position and confidence from each completed agent."""
        positions: dict[str, dict[str, Any]] = {}

        for agent_id, result in context.agent_results.items():
            if result.status != "completed" or result.response is None:
                continue

            response = result.response
            position = str(response.get("position", "neutral")).lower()

            # Handle enum-style values like "Position.SUPPORT"
            if "." in position:
                position = position.split(".")[-1].lower()

            confidence = float(response.get("confidence", 0.5))

            positions[agent_id] = {
                "position": position,
                "confidence": confidence,
            }

        return positions

    def _count_positions(
        self, positions: dict[str, dict[str, Any]]
    ) -> dict[str, int]:
        """Count how many agents hold each position."""
        counts = {SUPPORT: 0, CONDITIONAL: 0, NEUTRAL: 0, OPPOSE: 0}

        for data in positions.values():
            pos = data["position"]
            if pos in counts:
                counts[pos] += 1
            else:
                counts[NEUTRAL] += 1

        return counts

    def _determine_decision(
        self,
        counts: dict[str, int],
        positions: dict[str, dict[str, Any]],
    ) -> tuple[str, float]:
        """Apply deterministic decision rules.

        Returns (decision, confidence).
        """
        total = sum(counts.values())
        if total == 0:
            return "executive_review_required", 0.0

        support_ratio = counts[SUPPORT] / total
        support_conditional_ratio = (counts[SUPPORT] + counts[CONDITIONAL]) / total
        oppose_ratio = counts[OPPOSE] / total

        # Calculate weighted confidence from agent confidence scores
        avg_confidence = sum(
            d["confidence"] for d in positions.values()
        ) / len(positions)

        # Decision rules
        if support_ratio > 0.7:
            return "approved", min(avg_confidence + 0.1, 1.0)

        if support_conditional_ratio > 0.5 and oppose_ratio < 0.3:
            return "conditional_approval", avg_confidence

        if oppose_ratio > 0.5:
            return "rejected", avg_confidence

        # No clear majority
        return "executive_review_required", max(avg_confidence - 0.1, 0.0)

    def _detect_conflicts(
        self, positions: dict[str, dict[str, Any]]
    ) -> tuple[bool, list[dict[str, str]]]:
        """Detect conflicting positions between agents.

        A conflict exists when one agent supports and another opposes.
        """
        supporters = [
            aid for aid, d in positions.items() if d["position"] == SUPPORT
        ]
        opposers = [
            aid for aid, d in positions.items() if d["position"] == OPPOSE
        ]

        if not supporters or not opposers:
            return False, []

        # Build conflict pairs
        conflicts: list[dict[str, str]] = []
        for supporter in supporters:
            for opposer in opposers:
                conflicts.append({
                    "agent_supporting": supporter,
                    "agent_opposing": opposer,
                })

        return True, conflicts

    def _aggregate_risks(self, context: BoardContext) -> list[str]:
        """Aggregate and deduplicate risks from all agents."""
        all_risks: list[str] = []
        seen_normalized: set[str] = set()

        for agent_id, result in context.agent_results.items():
            if result.status != "completed" or result.response is None:
                continue

            response = result.response
            risks = response.get("risks", [])

            for risk in risks:
                if not isinstance(risk, str):
                    continue
                normalized = risk.lower().strip()
                # Simple deduplication by checking prefix similarity
                if normalized[:50] not in seen_normalized:
                    seen_normalized.add(normalized[:50])
                    # Add agent attribution
                    agent_label = agent_id.replace("_", " ").title()
                    all_risks.append(f"[{agent_label}] {risk}")

        return all_risks[:15]  # Cap at 15 most relevant risks

    def _aggregate_actions(self, context: BoardContext) -> list[str]:
        """Aggregate and deduplicate recommended actions from all agents."""
        all_actions: list[str] = []
        seen_normalized: set[str] = set()

        # Collect from various agent-specific action fields
        action_fields = [
            "conditions",
            "recommended_actions",
            "change_management_needs",
            "implementation_phases",
            "required_safeguards",
            "metrics_to_track",
        ]

        for agent_id, result in context.agent_results.items():
            if result.status != "completed" or result.response is None:
                continue

            response = result.response

            # Prioritize conditions as they represent requirements for support
            conditions = response.get("conditions", [])
            for item in conditions:
                if not isinstance(item, str):
                    continue
                normalized = item.lower().strip()
                if normalized[:50] not in seen_normalized:
                    seen_normalized.add(normalized[:50])
                    agent_label = agent_id.replace("_", " ").title()
                    all_actions.append(f"[{agent_label}] {item}")

        # Then collect from other action fields
        for agent_id, result in context.agent_results.items():
            if result.status != "completed" or result.response is None:
                continue

            response = result.response

            for field in action_fields:
                if field == "conditions":
                    continue  # Already processed
                items = response.get(field, [])
                if not isinstance(items, list):
                    continue
                for item in items:
                    if not isinstance(item, str):
                        continue
                    normalized = item.lower().strip()
                    if normalized[:50] not in seen_normalized:
                        seen_normalized.add(normalized[:50])
                        agent_label = agent_id.replace("_", " ").title()
                        all_actions.append(f"[{agent_label}] {item}")

        return all_actions[:20]  # Cap at 20 actions

    def _build_summary(
        self,
        decision: str,
        counts: dict[str, int],
        conflicting_agents: list[dict[str, str]],
        context: BoardContext,
    ) -> str:
        """Build a human-readable executive summary from structured data."""
        total = sum(counts.values())

        # Decision statement
        decision_text = {
            "approved": "The board recommends proceeding with this proposal.",
            "conditional_approval": (
                "The board recommends proceeding with conditions that must be addressed."
            ),
            "rejected": "The board recommends against proceeding with this proposal.",
            "executive_review_required": (
                "No clear consensus was reached. Executive review is required."
            ),
        }

        summary_parts = [decision_text.get(decision, "Decision pending.")]

        # Position breakdown
        breakdown_parts = []
        if counts[SUPPORT] > 0:
            breakdown_parts.append(f"{counts[SUPPORT]} department(s) support")
        if counts[CONDITIONAL] > 0:
            breakdown_parts.append(f"{counts[CONDITIONAL]} conditionally support")
        if counts[NEUTRAL] > 0:
            breakdown_parts.append(f"{counts[NEUTRAL]} are neutral")
        if counts[OPPOSE] > 0:
            breakdown_parts.append(f"{counts[OPPOSE]} oppose")

        if breakdown_parts:
            summary_parts.append(
                f"Of {total} participating departments: {', '.join(breakdown_parts)}."
            )

        # Conflict note
        if conflicting_agents:
            supporters = set(c["agent_supporting"] for c in conflicting_agents)
            opposers = set(c["agent_opposing"] for c in conflicting_agents)
            sup_names = ", ".join(a.replace("_", " ").title() for a in supporters)
            opp_names = ", ".join(a.replace("_", " ").title() for a in opposers)
            summary_parts.append(
                f"Conflict detected: {sup_names} support while {opp_names} oppose."
            )

        # Key concerns from opposing agents
        opposing_concerns = []
        for agent_id, result in context.agent_results.items():
            if result.status != "completed" or result.response is None:
                continue
            pos = str(result.response.get("position", "")).lower()
            if "." in pos:
                pos = pos.split(".")[-1].lower()
            if pos == OPPOSE:
                summary_text = result.response.get("summary", "")
                if summary_text:
                    agent_label = agent_id.replace("_", " ").title()
                    opposing_concerns.append(f"{agent_label} notes: {summary_text}")

        if opposing_concerns:
            summary_parts.append(" ".join(opposing_concerns[:2]))

        return " ".join(summary_parts)
