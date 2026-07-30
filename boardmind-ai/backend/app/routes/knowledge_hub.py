"""MCP Knowledge Hub API routes.

Provides endpoints for:
- Session history with full details
- Historical meeting queries
- Evidence retrieval
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import Response
from typing import Any
import base64

from sqlalchemy import select

from app.mcp_hub.integration import (
    get_historical_context,
    get_evidence_for_agent,
    get_history_service,
)
from app.mcp_hub.database import is_database_ready, get_session
from app.mcp_hub.models import Meeting, ExecutiveAnalysis, ConsensusRecord

router = APIRouter()


@router.get("/status")
async def hub_status() -> dict[str, Any]:
    """Check if the MCP Knowledge Hub is operational."""
    return {
        "configured": is_database_ready(),
        "message": "PostgreSQL connected" if is_database_ready() else "No database configured",
    }


@router.get("/history")
async def get_meeting_history(
    limit: int = Query(default=50, ge=1, le=100),
) -> dict[str, Any]:
    """Get recent session history with full details."""
    if not is_database_ready():
        return {"sessions": [], "count": 0}

    try:
        async with get_session() as session:
            # Get meetings
            meetings_result = await session.execute(
                select(Meeting).order_by(Meeting.created_at.desc()).limit(limit)
            )
            meetings = meetings_result.scalars().all()

            sessions_list = []
            for m in meetings:
                # Get analyses for this meeting
                analyses_result = await session.execute(
                    select(ExecutiveAnalysis).where(ExecutiveAnalysis.meeting_id == m.meeting_id)
                )
                analyses = analyses_result.scalars().all()

                # Get consensus
                consensus_result = await session.execute(
                    select(ConsensusRecord).where(ConsensusRecord.meeting_id == m.meeting_id)
                )
                consensus = consensus_result.scalar_one_or_none()

                sessions_list.append({
                    "session_id": m.meeting_id,
                    "title": m.title,
                    "scenario": m.proposal[:200],
                    "business_category": m.business_category,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                    "mode": "boardroom" if consensus else "workspace",
                    "has_report": m.report_json is not None,
                    "agents": [
                        {
                            "agent_id": a.executive_role,
                            "position": a.recommendation,
                            "confidence": a.confidence,
                        }
                        for a in analyses
                    ],
                    "consensus": {
                        "decision": consensus.decision,
                        "confidence": consensus.confidence,
                        "summary": consensus.summary[:150] if consensus.summary else None,
                    } if consensus else None,
                })

            return {"sessions": sessions_list, "count": len(sessions_list)}

    except Exception as e:
        return {"sessions": [], "count": 0, "error": str(e)}


@router.get("/session/{session_id}")
async def get_session_detail(session_id: str) -> dict[str, Any]:
    """Get full details of a specific session."""
    if not is_database_ready():
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        async with get_session() as session:
            # Get meeting
            meeting_result = await session.execute(
                select(Meeting).where(Meeting.meeting_id == session_id)
            )
            meeting = meeting_result.scalar_one_or_none()
            if not meeting:
                raise HTTPException(status_code=404, detail="Session not found")

            # Get analyses
            analyses_result = await session.execute(
                select(ExecutiveAnalysis).where(ExecutiveAnalysis.meeting_id == session_id)
            )
            analyses = analyses_result.scalars().all()

            # Get consensus
            consensus_result = await session.execute(
                select(ConsensusRecord).where(ConsensusRecord.meeting_id == session_id)
            )
            consensus = consensus_result.scalar_one_or_none()

            return {
                "session_id": meeting.meeting_id,
                "title": meeting.title,
                "scenario": meeting.proposal,
                "business_category": meeting.business_category,
                "created_at": meeting.created_at.isoformat() if meeting.created_at else None,
                "agents": [
                    {
                        "agent_id": a.executive_role,
                        "position": a.recommendation,
                        "confidence": a.confidence,
                        "rationale": a.rationale,
                        "risks": a.risks,
                        "conditions": a.supporting_conditions,
                        "actions": a.recommended_actions,
                    }
                    for a in analyses
                ],
                "consensus": {
                    "decision": consensus.decision,
                    "confidence": consensus.confidence,
                    "summary": consensus.summary,
                    "votes": consensus.votes,
                    "participating_agents": consensus.participating_agents,
                    "conflict_detected": consensus.conflict_detected,
                } if consensus else None,
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_similar_meetings(
    query: str = Query(..., min_length=5),
    limit: int = Query(default=5, ge=1, le=20),
) -> dict[str, Any]:
    """Search for similar past meetings."""
    results = await get_historical_context(query, limit=limit)
    return {"results": results, "count": len(results)}


@router.get("/report/{session_id}")
async def download_stored_report(session_id: str):
    """Download a stored report PDF from PostgreSQL."""
    if not is_database_ready():
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        async with get_session() as session:
            result = await session.execute(
                select(Meeting).where(Meeting.meeting_id == session_id)
            )
            meeting = result.scalar_one_or_none()

            if not meeting:
                raise HTTPException(status_code=404, detail="Session not found")

            if not meeting.report_pdf:
                raise HTTPException(status_code=404, detail="No report available for this session")

            pdf_bytes = base64.b64decode(meeting.report_pdf)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=boardmind-report-{session_id[:8]}.pdf"
                },
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evidence/{agent_id}")
async def get_agent_evidence(
    agent_id: str,
    meeting_id: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    """Get domain-specific evidence for an agent."""
    evidence = await get_evidence_for_agent(agent_id, meeting_id=meeting_id)
    return {"agent_id": agent_id, "evidence": evidence[:limit], "count": len(evidence)}
