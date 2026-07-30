"""Executive Orchestrator service.

Coordinates the execution of multiple department agents using a
dynamic worker pool architecture for maximum throughput:
1. Invokes the Decision Router to determine relevant agents
2. Creates a Board Context session
3. Builds prioritized task queue for all selected agents
4. Executes via async worker pool with API key load balancing
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
from app.agents.ceo import CEOAgentService, CEOAgentRequest
from app.agents.ciso import CISOAgentService, CISOAgentRequest
from app.agents.risk import RiskAgentService, RiskAgentRequest
from app.agents.compliance import ComplianceAgentService, ComplianceAgentRequest
from app.agents.strategy import StrategyAgentService, StrategyAgentRequest
from app.agents.product import ProductAgentService, ProductAgentRequest
from app.agents.customer_success import CustomerSuccessAgentService, CustomerSuccessAgentRequest
from app.agents.supply_chain import SupplyChainAgentService, SupplyChainAgentRequest
from app.agents.esg import ESGAgentService, ESGAgentRequest
from app.agents.ai_governance import AIGovernanceAgentService, AIGovernanceAgentRequest
from app.agents.innovation import InnovationAgentService, InnovationAgentRequest
from app.agents.investor_relations import InvestorRelationsAgentService, InvestorRelationsAgentRequest

from .schema import (
    OrchestratorRequest,
    OrchestratorResponse,
    AgentExecutionResult,
    ExecutionSummary,
)

logger = logging.getLogger(__name__)

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
    "ceo": ["strategy", "vision", "priority", "stakeholder", "competitive", "leadership", "growth", "transformation"],
    "ciso": ["security", "cyber", "threat", "vulnerability", "breach", "encryption", "soc2", "iso27001", "nist"],
    "risk": ["risk", "probability", "exposure", "mitigation", "scenario", "appetite", "tolerance", "downside"],
    "compliance": ["regulation", "compliance", "gdpr", "hipaa", "sox", "pci", "audit", "governance", "policy"],
    "strategy": ["market", "competitive", "strategy", "positioning", "growth", "tam", "differentiation", "moat"],
    "product": ["product", "feature", "roadmap", "user", "mvp", "adoption", "retention", "ux", "nps"],
    "customer_success": ["customer", "churn", "retention", "nps", "csat", "satisfaction", "onboarding", "renewal"],
    "supply_chain": ["supply", "vendor", "procurement", "logistics", "inventory", "warehouse", "fulfillment"],
    "esg": ["carbon", "emission", "sustainability", "esg", "climate", "diversity", "governance", "environmental"],
    "ai_governance": ["ai", "bias", "fairness", "ethics", "algorithmic", "explainability", "model", "responsible"],
    "innovation": ["innovation", "r&d", "research", "patent", "emerging", "prototype", "breakthrough", "novel"],
    "investor_relations": ["investor", "shareholder", "earnings", "eps", "guidance", "analyst", "market cap", "dividend"],
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
    """Coordinates dynamic worker pool execution of department agents.

    Uses a priority queue and async worker pool for maximum throughput
    with automatic API key load balancing and retry logic.

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
            "ceo": (CEOAgentService(), CEOAgentRequest),
            "ciso": (CISOAgentService(), CISOAgentRequest),
            "risk": (RiskAgentService(), RiskAgentRequest),
            "compliance": (ComplianceAgentService(), ComplianceAgentRequest),
            "strategy": (StrategyAgentService(), StrategyAgentRequest),
            "product": (ProductAgentService(), ProductAgentRequest),
            "customer_success": (CustomerSuccessAgentService(), CustomerSuccessAgentRequest),
            "supply_chain": (SupplyChainAgentService(), SupplyChainAgentRequest),
            "esg": (ESGAgentService(), ESGAgentRequest),
            "ai_governance": (AIGovernanceAgentService(), AIGovernanceAgentRequest),
            "innovation": (InnovationAgentService(), InnovationAgentRequest),
            "investor_relations": (InvestorRelationsAgentService(), InvestorRelationsAgentRequest),
        }

    @property
    def board_context(self) -> BoardContextService:
        """Expose board context for external read access (future modules)."""
        return self._board_context

    async def orchestrate(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Execute the full orchestration workflow using dynamic worker pool.

        All selected agents execute via a priority queue and worker pool.
        No agent is skipped. No wave-based delays. Maximum throughput.
        """
        from app.orchestrator.api_key_manager import APIKeyManager
        from app.orchestrator.worker_pool import WorkerPool, ExecutiveTask, PRIORITY_TIERS

        session_id = str(uuid.uuid4())
        meeting_start = time.perf_counter()

        # Step 1: Route the scenario
        router_request = DecisionRouterRequest(scenario=request.scenario)
        routing = self._router.route(router_request)
        routing_time_ms = int((time.perf_counter() - meeting_start) * 1000)

        # Step 2: Select agents (all 20 by default)
        if request.include_all_agents:
            selected_agents = list(self._agents.keys())
        else:
            selected_agents = routing.recommended_agents

        logger.info(
            f"Session {session_id}: {routing.business_category}, "
            f"{len(selected_agents)} agents selected, routing={routing_time_ms}ms"
        )

        # Step 3: Create Board Context session
        self._board_context.create_session(
            session_id=session_id,
            scenario=request.scenario,
            business_category=routing.business_category,
            selected_agents=selected_agents,
            optional_context=request.optional_context,
        )

        # Step 4: Build executive tasks with priority
        tasks = []
        for agent_id in selected_agents:
            if agent_id not in self._agents:
                continue
            service, request_cls = self._agents[agent_id]
            # Build request
            kwargs: dict[str, Any] = {"scenario": request.scenario}
            ctx = _filter_evidence_for_agent(request.optional_context, agent_id)
            if ctx:
                kwargs["context"] = ctx
            agent_request = request_cls(**kwargs)

            tasks.append(ExecutiveTask(
                agent_id=agent_id,
                priority=PRIORITY_TIERS.get(agent_id, 3),
                service=service,
                request=agent_request,
            ))

        # Step 5: Execute via Worker Pool
        key_manager = APIKeyManager()
        pool = WorkerPool(key_manager)

        async def board_context_updater(agent_id, status, response, time_ms, error):
            if status == "completed":
                await self._board_context.update_agent_response(
                    session_id=session_id, agent_id=agent_id,
                    response=response, execution_time_ms=time_ms, status="completed",
                )
            else:
                await self._board_context.update_agent_response(
                    session_id=session_id, agent_id=agent_id,
                    response=None, execution_time_ms=time_ms,
                    status=status, error=error,
                )

        # Mark all agents as started
        for task in tasks:
            await self._board_context.mark_agent_started(session_id, task.agent_id)

        results = await pool.execute_all(tasks, board_context_updater)

        total_time_ms = int((time.perf_counter() - meeting_start) * 1000)

        # Step 6: Finalize
        await self._board_context.finalize_session(session_id, total_time_ms)

        # Step 7: Build response
        completed = sum(1 for r in results if r.status == "completed")
        failed = sum(1 for r in results if r.status != "completed")

        # Convert to AgentExecutionResult
        agent_results = [
            AgentExecutionResult(
                agent_id=r.agent_id,
                response=r.response,
                execution_time_ms=r.execution_time_ms,
                status=r.status,
                error=r.error,
            )
            for r in results
        ]

        summary = ExecutionSummary(
            total_agents_selected=len(selected_agents),
            total_agents_completed=completed,
            total_agents_failed=failed,
            total_execution_time_ms=total_time_ms,
        )

        # Execution logging
        logger.info(
            f"Session {session_id}: COMPLETE — "
            f"{completed}/{len(results)} succeeded, {failed} failed, "
            f"{total_time_ms}ms total | "
            f"Keys: {key_manager.get_stats()}"
        )
        if failed > 0:
            failed_ids = [r.agent_id for r in results if r.status != "completed"]
            logger.warning(f"Session {session_id}: Failed: {failed_ids}")

        return OrchestratorResponse(
            session_id=session_id,
            scenario=request.scenario,
            business_category=routing.business_category,
            selected_agents=selected_agents,
            execution_summary=summary,
            responses=agent_results,
        )
