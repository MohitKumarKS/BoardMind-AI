"""Board Context module.

Provides in-memory shared state for executive board meetings.
Each session stores the complete deliberation state including
scenario, routing, agent results, execution metadata, and consensus.

The Orchestrator is the only writer for agent results.
The Consensus Engine writes the consensus_result.

Usage:
    from app.board_context import BoardContextService

    ctx = BoardContextService()
    session = ctx.create_session(session_id, scenario, category, agents)
    await ctx.update_agent_response(session_id, agent_id, response, time_ms)
    context = ctx.get_context(session_id)
"""

from .schema import BoardContext, AgentResult, ExecutionMetadata, ConsensusResult
from .service import BoardContextService

__all__ = [
    "BoardContextService",
    "BoardContext",
    "AgentResult",
    "ExecutionMetadata",
    "ConsensusResult",
]
