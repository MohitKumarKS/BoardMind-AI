"""MCP Knowledge Hub integration hooks.

These are called AFTER the existing orchestration/consensus completes.
They persist data to PostgreSQL without modifying the existing flow.
If the database is unavailable, all operations are silently skipped.
"""

import logging
from typing import Any

from .database import is_database_ready
from .storage_service import StorageService
from .evidence_service import EvidenceService
from .history_service import HistoryService

logger = logging.getLogger(__name__)

# Module-level singleton services
_storage = StorageService()
_evidence = EvidenceService()
_history = HistoryService()


async def persist_meeting_results(
    session_id: str,
    scenario: str,
    business_category: str,
    agent_responses: list[dict[str, Any]],
    consensus_result: dict[str, Any] | None = None,
    optional_context: str | None = None,
) -> None:
    """Persist full meeting results to PostgreSQL.

    Called after consensus completes. Silently does nothing if
    the database is not configured or available.

    Args:
        session_id: The meeting/session ID.
        scenario: The business scenario text.
        business_category: Classified category.
        agent_responses: List of AgentExecutionResult dicts.
        consensus_result: Optional consensus result dict.
        optional_context: Optional user context.
    """
    if not is_database_ready():
        return

    try:
        # Store meeting
        await _storage.store_meeting(
            meeting_id=session_id,
            proposal=scenario,
            business_category=business_category,
            optional_context=optional_context,
        )

        # Store each agent analysis
        for resp in agent_responses:
            if resp.get("status") == "completed" and resp.get("response"):
                await _storage.store_analysis(
                    meeting_id=session_id,
                    executive_role=resp["agent_id"],
                    response=resp["response"],
                )

        # Store consensus
        if consensus_result:
            await _storage.store_consensus(
                meeting_id=session_id,
                consensus=consensus_result,
            )

        logger.info(f"MCP Hub: Meeting {session_id[:8]} persisted to PostgreSQL")

    except Exception as e:
        logger.error(f"MCP Hub persistence failed (non-fatal): {e}")


async def get_historical_context(query: str, limit: int = 3) -> list[dict[str, Any]]:
    """Retrieve historical meetings similar to the query.

    Returns empty list if database is unavailable or no matches found.
    """
    if not is_database_ready():
        return []

    return await _history.find_similar_meetings(query, limit=limit)


async def get_evidence_for_agent(agent_id: str, meeting_id: str | None = None) -> list[dict[str, Any]]:
    """Retrieve domain-specific evidence for an agent.

    Returns empty list if database is unavailable.
    """
    if not is_database_ready():
        return []

    return await _evidence.get_evidence_for_agent(agent_id, meeting_id=meeting_id)


def get_storage_service() -> StorageService:
    """Get the storage service instance."""
    return _storage


def get_evidence_service() -> EvidenceService:
    """Get the evidence service instance."""
    return _evidence


def get_history_service() -> HistoryService:
    """Get the history service instance."""
    return _history
