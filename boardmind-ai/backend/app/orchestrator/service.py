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
import os
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

# Wave configuration: production-optimized for 20 agents
# Strategy: small waves with proper backoff allow all agents to get real LLM responses
# The retry logic handles rate limits via exponential backoff
WAVE_SIZE = int(os.environ.get("WAVE_SIZE", "3"))  # 3 agents per wave
INTER_WAVE_BASE_DELAY = float(os.environ.get("INTER_WAVE_DELAY", "10.0"))  # 10s between waves (TPM recovery)
RATE_LIMIT_EXTRA_DELAY = 8.0  # additional delay if 429 detected in wave
AGENT_TIMEOUT_SECONDS = float(os.environ.get("AGENT_TIMEOUT", "45.0"))  # 45s to allow retries
INTRA_WAVE_STAGGER = 1.0  # 1s stagger between agent starts within wave

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
    "ceo": ["strategy", "vision", "priority", "stakeholder", "competitive", "leadership", "direction", "growth", "transformation"],
    "ciso": ["security", "cyber", "threat", "vulnerability", "breach", "encryption", "attack", "soc2", "iso27001", "nist", "access"],
    "risk": ["risk", "probability", "exposure", "mitigation", "scenario", "monte carlo", "appetite", "tolerance", "downside"],
    "compliance": ["regulation", "compliance", "gdpr", "hipaa", "sox", "pci", "audit", "governance", "policy", "standard"],
    "strategy": ["market", "competitive", "strategy", "positioning", "growth", "tam", "differentiation", "moat", "advantage"],
    "product": ["product", "feature", "roadmap", "user", "mvp", "adoption", "retention", "ux", "nps", "backlog"],
    "customer_success": ["customer", "churn", "retention", "nps", "csat", "satisfaction", "onboarding", "health score", "renewal"],
    "supply_chain": ["supply", "vendor", "procurement", "logistics", "inventory", "warehouse", "fulfillment", "lead time", "sourcing"],
    "esg": ["carbon", "emission", "sustainability", "esg", "climate", "diversity", "governance", "green", "social", "environmental"],
    "ai_governance": ["ai", "bias", "fairness", "ethics", "algorithmic", "explainability", "model", "ml", "responsible ai", "governance"],
    "innovation": ["innovation", "r&d", "research", "patent", "emerging", "prototype", "breakthrough", "novel", "experiment"],
    "investor_relations": ["investor", "shareholder", "earnings", "eps", "guidance", "analyst", "market cap", "dividend", "valuation"],
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
        self._last_rate_limit_time: float = 0

    @property
    def board_context(self) -> BoardContextService:
        """Expose board context for external read access (future modules)."""
        return self._board_context

    async def orchestrate(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Execute the full orchestration workflow with wave-based scheduling.

        1. Route scenario via Decision Router
        2. If include_all_agents=True, use all 20 agents
        3. Create Board Context session
        4. Split agents into waves of WAVE_SIZE
        5. Execute each wave with parallel agents, sequential waves
        6. Apply dynamic inter-wave delay based on rate limit detection
        7. Finalize session and return aggregated results
        """
        session_id = str(uuid.uuid4())

        # Step 1: Route the scenario
        router_request = DecisionRouterRequest(scenario=request.scenario)
        routing = self._router.route(router_request)

        # Step 2: Determine agent list
        if request.include_all_agents:
            # Full board meeting — all 20 executives participate
            recommended_agents = list(self._agents.keys())
        else:
            recommended_agents = routing.recommended_agents

        logger.info(
            f"Session {session_id}: Category='{routing.business_category}', "
            f"Agents={len(recommended_agents)} ({'full board' if request.include_all_agents else 'selective'})"
        )

        # Step 3: Create Board Context session
        self._board_context.create_session(
            session_id=session_id,
            scenario=request.scenario,
            business_category=routing.business_category,
            selected_agents=recommended_agents,
            optional_context=request.optional_context,
        )

        # Step 4: Wave-based execution
        start_time = time.perf_counter()

        valid_agents = [
            agent_id
            for agent_id in recommended_agents
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

            # Execute wave agents with staggered starts to prevent burst
            tasks = []
            for idx, agent_id in enumerate(wave_agents):
                # Stagger start: each agent delayed by INTRA_WAVE_STAGGER * idx
                tasks.append(
                    self._execute_agent_staggered(
                        session_id, agent_id, request.scenario,
                        _filter_evidence_for_agent(request.optional_context, agent_id),
                        delay=INTRA_WAVE_STAGGER * idx,
                    )
                )

            wave_results = await asyncio.gather(*tasks)
            all_results.extend(wave_results)

            # Check if any agent in this wave hit a rate limit
            for r in wave_results:
                if r.error and "429" in (r.error or ""):
                    self._last_rate_limit_time = time.perf_counter()

        total_time_ms = int((time.perf_counter() - start_time) * 1000)

        # Step 5: Finalize Board Context
        await self._board_context.finalize_session(session_id, total_time_ms)

        # Step 6: Build execution summary
        completed = sum(1 for r in all_results if r.status == "completed")
        failed = sum(1 for r in all_results if r.status != "completed")

        summary = ExecutionSummary(
            total_agents_selected=len(recommended_agents),
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
            selected_agents=recommended_agents,
            execution_summary=summary,
            responses=all_results,
        )

    def _calculate_inter_wave_delay(self) -> float:
        """Calculate dynamic delay between waves.

        Only adds extra delay if a recent 429 was detected.
        Otherwise uses minimal delay to maximize throughput.
        """
        now = time.perf_counter()
        time_since_rate_limit = now - self._last_rate_limit_time

        if time_since_rate_limit < 20:
            # Recent rate limit — add extra cooldown
            return INTER_WAVE_BASE_DELAY + RATE_LIMIT_EXTRA_DELAY
        return INTER_WAVE_BASE_DELAY

    async def _execute_agent_staggered(
        self,
        session_id: str,
        agent_id: str,
        scenario: str,
        context: str | None,
        delay: float = 0.0,
    ) -> AgentExecutionResult:
        """Execute agent with an initial stagger delay to prevent burst."""
        if delay > 0:
            await asyncio.sleep(delay)
        return await self._execute_agent(session_id, agent_id, scenario, context)

    async def _execute_agent(
        self,
        session_id: str,
        agent_id: str,
        scenario: str,
        context: str | None,
    ) -> AgentExecutionResult:
        """Execute a single agent and update Board Context.

        Uses compact prompts for production efficiency, falling through
        to the agent's standard analyze() as backup.
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

            # Execute the agent with timeout protection
            response = await asyncio.wait_for(
                service.analyze(agent_request),
                timeout=AGENT_TIMEOUT_SECONDS,
            )
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

        except asyncio.TimeoutError:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            error_msg = f"Agent '{agent_id}' timed out after {AGENT_TIMEOUT_SECONDS}s"
            logger.error(error_msg)

            await self._board_context.update_agent_response(
                session_id=session_id,
                agent_id=agent_id,
                response=None,
                execution_time_ms=elapsed_ms,
                status="timeout",
                error=error_msg,
            )

            return AgentExecutionResult(
                agent_id=agent_id,
                response=None,
                execution_time_ms=elapsed_ms,
                status="timeout",
                error=error_msg,
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
