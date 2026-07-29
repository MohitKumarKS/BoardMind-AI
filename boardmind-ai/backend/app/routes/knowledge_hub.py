"""MCP Knowledge Hub API routes.

Provides endpoints for:
- Historical meeting queries
- Evidence retrieval
- Meeting history listing

These are purely additive — existing APIs remain unchanged.
"""

from fastapi import APIRouter, Query
from typing import Any

from app.mcp_hub.integration import (
    get_historical_context,
    get_evidence_for_agent,
    get_history_service,
)
from app.mcp_hub.database import is_database_ready

router = APIRouter()


@router.get("/status")
async def hub_status() -> dict[str, Any]:
    """Check if the MCP Knowledge Hub is operational."""
    return {
        "configured": is_database_ready(),
        "message": "PostgreSQL connected" if is_database_ready() else "No database configured — running in memory-only mode",
    }


@router.get("/history")
async def get_meeting_history(
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    """Get recent meeting history."""
    history = await get_history_service().get_meeting_history(limit=limit)
    return {"meetings": history, "count": len(history)}


@router.get("/search")
async def search_similar_meetings(
    query: str = Query(..., min_length=5, description="Search terms for finding similar meetings"),
    limit: int = Query(default=5, ge=1, le=20),
) -> dict[str, Any]:
    """Search for similar past meetings."""
    results = await get_historical_context(query, limit=limit)
    return {"results": results, "count": len(results)}


@router.get("/evidence/{agent_id}")
async def get_agent_evidence(
    agent_id: str,
    meeting_id: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    """Get domain-specific evidence for an agent."""
    evidence = await get_evidence_for_agent(agent_id, meeting_id=meeting_id)
    return {"agent_id": agent_id, "evidence": evidence[:limit], "count": len(evidence)}
