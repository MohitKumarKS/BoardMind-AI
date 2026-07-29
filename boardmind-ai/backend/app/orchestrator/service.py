"""Executive Orchestrator service.

Coordinates the execution of multiple department agents using
wave-based scheduling to stay within Groq TPM rate limits:
1. Invokes the Decision Router to determine relevant agents
2. Creates a Board Context session
3. Executes agents in sequential waves (4 per wave, parallel within wave)
4. Applies dynamic inter-wave delay if rate limits are detected
5. Updates Board Context after each agent completes
6. Finalizes the session and returns results

The Orchestrator does NOT modify or interpret agent responses.
It is purely a coordination layer and the ONLY writer to Board Context.
"""

import asyncio
import logging
import time
import uuid
from typing import Any

from app.decision_router import DecisionRouterService, DecisionRouterRequest
from app.board_context import BoardContextService
from app.agents.finance import FinanceAgentService, FinanceAgentRequest
from app.agents.marketing import MarketingAgentService, MarketingAgentRequest
from app.agents.sales import SalesAgentService, SalesAgentRequest
from app.agents.hr import HRAgentService, HRAgentRequest
from app.agents.operations import OperationsAgentService, OperationsAgentRequest
from app.agents.legal import LegalAgentService, LegalAgentRequest
from app.agents.it import ITAgentService, ITAgentRequest
from app.agents.business_analytics import AnalyticsAgentService, AnalyticsAgentRequest

from .schema import (
    OrchestratorRequest,
    OrchestratorResponse,
    AgentExecutionResult,
    ExecutionSummary,
)

logger = logging.getLogger(__name__)

# Wave configuration: agents are split into waves to avoid TPM limits
WAVE_SIZE = 4
INTER_WAVE_BASE_DELAY = 5.0  # seconds between waves (minimum cooldown)
RATE_LIMIT_EXTRA_DELAY = 12.0  # additional delay if 429 detected in wave

# Domain-specific evidence keywords for filtering
DOMAIN_EVIDENCE_KEYWORDS: dict[str, list[str]] = {
    "finance": ["revenue", "cost", "budget", "roi", "profit", "margin", "price", "investment", "growth", "$"],
    "marketing": ["market", "brand", "customer", "segment", "campaign", "demand", "awareness", "positioning"],
    "sales": ["revenue", "pipeline", "deal", "customer", "demand", "unit", "quota", "account", "sale"],
    "hr": ["employee", "headcount", "team", "hire", "workforce", "staff", "talent", "training", "people"],
    "operations": ["region", "capacity", "supply", "logistics", "delivery", "volume", "process", "timeline"],
    "legal": ["compliance", "regulation", "gdpr", "contract", "privacy", "liability", "ip", "governance", "soc"],
    "it": ["technology", "system", "cloud", "security", "platform", "infrastructure", "api", "data", "software"],
    "business_analytics": ["metric", "kpi", "growth", "average", "total", "percent", "benchmark", "forecast", "data"],
}


def _filter_evidence_for_agent(context: str | None, agent_id: str) -> str | None:
    """Filter evidence context to include only domain-relevant lines.

    Reduces token usage by giving each agent only the evidence
    lines that match its domain expertise.
    """
    if not context or "[Attached File:" not in context:
        return context

    # Split into pre-evidence and evidence parts
    parts = context.split("[Attached File:", 1)
    user_context = parts[0].strip()
    evidence_section = "[Attached File:" + parts[1]

    # Get domain keywords for this agent
    keywords = DOMAIN_EVIDENCE_KEYWORDS.get(agent_id, [])
    if not keywords:
        return context

    # Filter evidence lines to only domain-relevant ones
    evidence_lines = evidence_section.split("\n")
    filtered_lines = []

    # Always keep the file header line and column info
    for line in evidence_lines:
        line_lower = line.lower()
        # Keep structural lines (headers, source info, column names)
        if any(marker in line_lower for marker in ["attached file:", "source:", "columns:", "top ", "rows"]):
            filtered_lines.append(line)
        # Keep lines containing domain-relevant keywords
        elif any(kw in line_lower for kw in keywords):
            filtered_lines.append(line)

    # Reconstruct with filtered evidence (max 800 chars)
    filtered_evidence = "\n".join(filtered_lines)[:800]

    if user_context:
        return f"{user_context}\n\n{filtered_evidence}"
    return filtered_evidence


class ExecutiveOrchestratorService:
    """Coordinates wave-based execution of department agents.

    Uses sequential waves to respect Groq TPM limits while maintaining
    parallelism within each wave.

    Usage:
        service = ExecutiveOrchestratorService()
        response = await service.orchestrate(request)
    """

    def __init__(self):
        self._router = DecisionRouterService()
        self._board_context = BoardContextService()
        self._agents: dict[str, Any] = {
            "finance": (FinanceAgentService(), FinanceAgentRequest),
            "marketing": (MarketingAgentService(), MarketingAgentRequest),
            "sales": (SalesAgentService(), SalesAgentRequest),
            "hr": (HRAgentService(), HRAgentRequest),
            "operations": (OperationsAgentService(), OperationsAgentRequest),
            "legal": (LegalAgentService(), LegalAgentRequest),
            "it": (ITAgentService(), ITAgentRequest),
            "business_analytics": (AnalyticsAgentService(), AnalyticsAgentRequest),
        }
        self._last_rate_limit_time: float = 0

    @property
    def board_context(self) -> BoardContextService:
        """Expose board context for external read access (future modules)."""
        return self._board_context

    async def orchestrate(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Execute the full orchestration workflow with wave-based scheduling.

        1. Route scenario via Decision Router
        2. Create Board Context session
        3. Split agents into waves of WAVE_SIZE
        4. Execute each wave with parallel agents, sequential waves
        5. Apply dynamic inter-wave delay based on rate limit detection
        6. Finalize session and return aggregated results
        """
        session_id = str(uuid.uuid4())

        # Step 1: Route the scenario
        router_request = DecisionRouterRequest(scenario=request.scenario)
        routing = self._router.route(router_request)

        logger.info(
            f"Session {session_id}: Category='{routing.business_category}', "
            f"Agents={routing.recommended_agents}"
        )

        # Step 2: Create Board Context session
        self._board_context.create_session(
            session_id=session_id,
            scenario=request.scenario,
            business_category=routing.business_category,
            selected_agents=routing.recommended_agents,
            optional_context=request.optional_context,
        )

        # Step 3: Wave-based execution
        start_time = time.perf_counter()

        valid_agents = [
            agent_id
            for agent_id in routing.recommended_agents
            if agent_id in self._agents
        ]

        # Split into waves
        waves = [valid_agents[i:i + WAVE_SIZE] for i in range(0, len(valid_agents), WAVE_SIZE)]
        all_results: list[AgentExecutionResult] = []

        for wave_idx, wave_agents in enumerate(waves):
            # Dynamic inter-wave delay
            if wave_idx > 0:
                delay = self._calculate_inter_wave_delay()
                logger.info(
                    f"Session {session_id}: Wave {wave_idx + 1} — "
                    f"waiting {delay:.1f}s before starting"
                )
                await asyncio.sleep(delay)

            logger.info(
                f"Session {session_id}: Wave {wave_idx + 1}/{len(waves)} — "
                f"executing {wave_agents}"
            )

            # Execute wave agents in parallel
            tasks = [
                self._execute_agent(
                    session_id, agent_id, request.scenario,
                    _filter_evidence_for_agent(request.optional_context, agent_id)
                )
                for agent_id in wave_agents
            ]

            wave_results = await asyncio.gather(*tasks)
            all_results.extend(wave_results)

            # Check if any agent in this wave hit a rate limit
            for r in wave_results:
                if r.error and "429" in (r.error or ""):
                    self._last_rate_limit_time = time.perf_counter()

        total_time_ms = int((time.perf_counter() - start_time) * 1000)

        # Step 4: Finalize Board Context
        await self._board_context.finalize_session(session_id, total_time_ms)

        # Step 5: Build execution summary
        completed = sum(1 for r in all_results if r.status == "completed")
        failed = sum(1 for r in all_results if r.status != "completed")

        summary = ExecutionSummary(
            total_agents_selected=len(routing.recommended_agents),
            total_agents_completed=completed,
            total_agents_failed=failed,
            total_execution_time_ms=total_time_ms,
        )

        logger.info(
            f"Session {session_id}: Completed {completed}/{len(all_results)} agents "
            f"in {total_time_ms}ms ({len(waves)} waves)"
        )

        return OrchestratorResponse(
            session_id=session_id,
            scenario=request.scenario,
            business_category=routing.business_category,
            selected_agents=routing.recommended_agents,
            execution_summary=summary,
            responses=all_results,
        )

    def _calculate_inter_wave_delay(self) -> float:
        """Calculate dynamic delay between waves.

        If a recent 429 was detected, add extra delay.
        Otherwise use the base delay.
        """
        now = time.perf_counter()
        time_since_rate_limit = now - self._last_rate_limit_time

        if time_since_rate_limit < 30:
            # Recent rate limit — add extra cooldown
            return INTER_WAVE_BASE_DELAY + RATE_LIMIT_EXTRA_DELAY
        return INTER_WAVE_BASE_DELAY

    async def _execute_agent(
        self,
        session_id: str,
        agent_id: str,
        scenario: str,
        context: str | None,
    ) -> AgentExecutionResult:
        """Execute a single agent and update Board Context.

        Handles errors gracefully — a failed agent does not break
        the entire orchestration.
        """
        # Mark agent as started in Board Context
        await self._board_context.mark_agent_started(session_id, agent_id)

        start = time.perf_counter()

        try:
            service, request_cls = self._agents[agent_id]

            # Build agent-specific request
            request_kwargs: dict[str, Any] = {"scenario": scenario}
            if context:
                request_kwargs["context"] = context

            agent_request = request_cls(**request_kwargs)

            # Execute the agent
            response = await service.analyze(agent_request)
            response_dict = response.model_dump()

            elapsed_ms = int((time.perf_counter() - start) * 1000)

            # Update Board Context with success
            await self._board_context.update_agent_response(
                session_id=session_id,
                agent_id=agent_id,
                response=response_dict,
                execution_time_ms=elapsed_ms,
                status="completed",
            )

            return AgentExecutionResult(
                agent_id=agent_id,
                response=response_dict,
                execution_time_ms=elapsed_ms,
                status="completed",
                error=None,
            )

        except Exception as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            error_msg = str(e)
            logger.error(f"Agent '{agent_id}' failed: {error_msg}")

            # Track rate limits for inter-wave delay calculation
            if "429" in error_msg:
                self._last_rate_limit_time = time.perf_counter()

            # Update Board Context with failure
            await self._board_context.update_agent_response(
                session_id=session_id,
                agent_id=agent_id,
                response=None,
                execution_time_ms=elapsed_ms,
                status="failed",
                error=error_msg,
            )

            return AgentExecutionResult(
                agent_id=agent_id,
                response=None,
                execution_time_ms=elapsed_ms,
                status="failed",
                error=error_msg,
            )
