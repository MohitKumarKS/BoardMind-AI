"""Consensus Engine module.

Analyzes completed Board Context and produces executive recommendations.
No LLM calls — purely deterministic logic over structured agent responses.

Usage:
    from app.consensus import ConsensusEngineService
    from app.board_context import BoardContextService

    board_ctx = BoardContextService()
    engine = ConsensusEngineService(board_ctx)
    result = engine.analyze(session_id)
"""

from .schema import ConsensusRequest
from .service import ConsensusEngineService

__all__ = [
    "ConsensusEngineService",
    "ConsensusRequest",
]
