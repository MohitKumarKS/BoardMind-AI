"""Executive Orchestrator module.

Coordinates the parallel execution of department agents selected
by the Decision Router. Does not interpret or modify agent responses.

Usage:
    from app.orchestrator import ExecutiveOrchestratorService, OrchestratorRequest

    service = ExecutiveOrchestratorService()
    response = await service.orchestrate(request)
"""

from .schema import (
    OrchestratorRequest,
    OrchestratorResponse,
    AgentExecutionResult,
    ExecutionSummary,
)
from .service import ExecutiveOrchestratorService

__all__ = [
    "ExecutiveOrchestratorService",
    "OrchestratorRequest",
    "OrchestratorResponse",
    "AgentExecutionResult",
    "ExecutionSummary",
]
