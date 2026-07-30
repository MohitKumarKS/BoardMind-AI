"""Board Context service.

In-memory session store for the shared state of executive board meetings.
Each session represents one orchestration run. Sessions are not persisted.

The Orchestrator is the ONLY writer. Future modules (Consensus Engine,
Report Generator) will read from this context.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Any

from .schema import BoardContext, AgentResult, ExecutionMetadata

logger = logging.getLogger(__name__)


class BoardContextService:
    """Manages in-memory board session state.

    Thread-safe via asyncio.Lock for concurrent agent updates.
    Sessions are automatically evicted when exceeding MAX_SESSIONS.

    Usage:
        ctx = BoardContextService()
        session = ctx.create_session(...)
        ctx.update_agent_response(session_id, agent_id, response)
        context = ctx.get_context(session_id)
    """

    MAX_SESSIONS = 200  # Evict oldest when exceeded

    def __init__(self):
        self._sessions: dict[str, BoardContext] = {}
        self._lock = asyncio.Lock()

    def create_session(
        self,
        session_id: str,
        scenario: str,
        business_category: str,
        selected_agents: list[str],
        optional_context: Optional[str] = None,
    ) -> BoardContext:
        """Create a new board session.

        Initializes the context with pending agent results for all
        selected agents.
        """
        now = datetime.utcnow()

        agent_results = {
            agent_id: AgentResult(agent_id=agent_id, status="pending")
            for agent_id in selected_agents
        }

        context = BoardContext(
            session_id=session_id,
            scenario=scenario,
            optional_context=optional_context,
            business_category=business_category,
            selected_agents=selected_agents,
            created_at=now,
            updated_at=now,
            status="in_progress",
            agent_results=agent_results,
            execution_metadata=ExecutionMetadata(
                total_agents=len(selected_agents),
            ),
        )

        self._sessions[session_id] = context
        self._evict_old_sessions()
        logger.info(f"Board Context created: session={session_id}, agents={selected_agents}")
        return context

    def _evict_old_sessions(self) -> None:
        """Remove oldest sessions when exceeding MAX_SESSIONS."""
        if len(self._sessions) <= self.MAX_SESSIONS:
            return
        # Sort by created_at and remove oldest
        sorted_sessions = sorted(
            self._sessions.items(),
            key=lambda item: item[1].created_at,
        )
        to_remove = len(self._sessions) - self.MAX_SESSIONS
        for session_id, _ in sorted_sessions[:to_remove]:
            del self._sessions[session_id]
            logger.debug(f"Evicted old session: {session_id}")

    def get_session(self, session_id: str) -> Optional[BoardContext]:
        """Retrieve a board session by ID. Returns None if not found."""
        return self._sessions.get(session_id)

    def get_context(self, session_id: str) -> Optional[BoardContext]:
        """Alias for get_session — used by future modules for reading context."""
        return self.get_session(session_id)

    async def mark_agent_started(self, session_id: str, agent_id: str) -> None:
        """Mark an agent as running."""
        async with self._lock:
            session = self._sessions.get(session_id)
            if session and agent_id in session.agent_results:
                session.agent_results[agent_id].status = "running"
                session.agent_results[agent_id].started_at = datetime.utcnow()
                session.updated_at = datetime.utcnow()

    async def update_agent_response(
        self,
        session_id: str,
        agent_id: str,
        response: Optional[dict[str, Any]],
        execution_time_ms: int,
        status: str = "completed",
        error: Optional[str] = None,
    ) -> None:
        """Update a specific agent's result in the board context.

        Called by the Orchestrator after each agent completes or fails.
        """
        async with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                logger.warning(f"Session {session_id} not found for agent update")
                return

            if agent_id not in session.agent_results:
                logger.warning(f"Agent {agent_id} not in session {session_id}")
                return

            now = datetime.utcnow()

            session.agent_results[agent_id] = AgentResult(
                agent_id=agent_id,
                status=status,
                started_at=session.agent_results[agent_id].started_at,
                completed_at=now,
                execution_time_ms=execution_time_ms,
                response=response,
                error=error,
            )

            # Update execution metadata
            completed = sum(
                1 for r in session.agent_results.values() if r.status == "completed"
            )
            failed = sum(
                1 for r in session.agent_results.values() if r.status == "failed"
            )
            session.execution_metadata.completed_agents = completed
            session.execution_metadata.failed_agents = failed

            session.updated_at = now

            logger.debug(
                f"Board Context updated: session={session_id}, "
                f"agent={agent_id}, status={status}"
            )

    def list_completed_agents(self, session_id: str) -> list[str]:
        """Return list of agent IDs that have completed successfully."""
        session = self._sessions.get(session_id)
        if not session:
            return []
        return [
            agent_id
            for agent_id, result in session.agent_results.items()
            if result.status == "completed"
        ]

    async def finalize_session(
        self, session_id: str, total_execution_time_ms: int
    ) -> Optional[BoardContext]:
        """Mark a session as completed and set final execution time.

        Called by the Orchestrator after all agents finish.
        """
        async with self._lock:
            session = self._sessions.get(session_id)
            if not session:
                return None

            session.status = "completed"
            session.execution_metadata.total_execution_time_ms = total_execution_time_ms
            session.updated_at = datetime.utcnow()

            # If any agents failed, mark session accordingly
            if session.execution_metadata.failed_agents > 0:
                if session.execution_metadata.completed_agents == 0:
                    session.status = "failed"

            logger.info(
                f"Board Context finalized: session={session_id}, "
                f"status={session.status}, "
                f"completed={session.execution_metadata.completed_agents}/"
                f"{session.execution_metadata.total_agents}"
            )
            return session

    def add_shared_note(self, session_id: str, note: str) -> None:
        """Add a shared meeting note to the session.

        For use by future modules (Consensus Engine, etc.).
        """
        session = self._sessions.get(session_id)
        if session:
            session.shared_notes.append(note)
            session.updated_at = datetime.utcnow()

    def add_mcp_source(self, session_id: str, source: dict) -> None:
        """Record an MCP data source used during the meeting.

        Args:
            session_id: The session to update.
            source: Dict describing the MCP resource (type, filename, metadata).
        """
        session = self._sessions.get(session_id)
        if session:
            session.mcp_sources.append(source)
            session.updated_at = datetime.utcnow()

    def get_mcp_sources(self, session_id: str) -> list[dict]:
        """Get all MCP data sources recorded for a session."""
        session = self._sessions.get(session_id)
        if session:
            return session.mcp_sources
        return []

    def clear_session(self, session_id: str) -> bool:
        """Remove a session from the store. Returns True if found and removed."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Board Context cleared: session={session_id}")
            return True
        return False

    def list_sessions(self) -> list[str]:
        """Return all active session IDs."""
        return list(self._sessions.keys())
