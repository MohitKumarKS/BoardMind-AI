"""Executive Boardroom API routes.

Provides endpoints for orchestrated multi-agent analysis and consensus.
"""

from fastapi import APIRouter, HTTPException

from app.orchestrator import (
    ExecutiveOrchestratorService,
    OrchestratorRequest,
    OrchestratorResponse,
)
from app.consensus import ConsensusEngineService, ConsensusRequest
from app.board_context import ConsensusResult
from app.routes.mcp import get_registry, get_and_clear_evidence_summary

router = APIRouter()

orchestrator = ExecutiveOrchestratorService()
consensus_engine = ConsensusEngineService(orchestrator.board_context)


@router.post("/orchestrate", response_model=OrchestratorResponse)
async def orchestrate(request: OrchestratorRequest) -> OrchestratorResponse:
    """Submit a business scenario for multi-department analysis.

    The orchestrator:
    1. Classifies the scenario via the Decision Router
    2. Selects relevant department agents
    3. Executes all selected agents concurrently
    4. Returns aggregated results

    Agents operate independently — no cross-agent communication occurs.
    If MCP data was uploaded prior to orchestration, sources are recorded
    in the Board Context.
    """
    try:
        result = await orchestrator.orchestrate(request)

        # Record any MCP sources that were used prior to this orchestration
        mcp_registry = get_registry()
        if mcp_registry.usage_log:
            for entry in mcp_registry.usage_log:
                orchestrator.board_context.add_mcp_source(result.session_id, entry)
            mcp_registry.clear_usage_log()

        # Store MCP evidence summary in Board Context for report generation
        evidence = get_and_clear_evidence_summary()
        if evidence:
            session = orchestrator.board_context.get_session(result.session_id)
            if session:
                session.mcp_evidence_summary = evidence

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Orchestration failed: {str(e)}",
        )


@router.post("/consensus", response_model=ConsensusResult)
async def run_consensus(request: ConsensusRequest) -> ConsensusResult:
    """Run the Consensus Engine on a completed orchestration session.

    Analyzes all department responses in the Board Context and produces:
    - Final decision (approved, conditional_approval, rejected, executive_review_required)
    - Conflict detection between departments
    - Aggregated risks and recommended actions
    - Executive summary

    The session must have been created via /api/boardroom/orchestrate first.
    After consensus, results are persisted to MCP Knowledge Hub (if configured).
    """
    try:
        result = consensus_engine.analyze(request.session_id)

        # Persist to MCP Knowledge Hub (non-blocking, fails gracefully)
        try:
            from app.mcp_hub.integration import persist_meeting_results

            # Get the board context for this session
            ctx = orchestrator.board_context.get_context(request.session_id)
            if ctx:
                agent_responses = [
                    {
                        "agent_id": aid,
                        "status": ar.status,
                        "response": ar.response,
                    }
                    for aid, ar in ctx.agent_results.items()
                ]

                await persist_meeting_results(
                    session_id=request.session_id,
                    scenario=ctx.scenario,
                    business_category=ctx.business_category,
                    agent_responses=agent_responses,
                    consensus_result=result.model_dump(),
                    optional_context=ctx.optional_context,
                )
        except Exception:
            pass  # Non-fatal — hub persistence is optional

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Consensus analysis failed: {str(e)}",
        )
