"""Department Workspace API routes.

Provides endpoints for single-agent analysis in Department Workspace mode.
Each agent operates independently — no orchestration or consensus.
Results are persisted to MCP Knowledge Hub when available.
"""

import uuid
import logging
from fastapi import APIRouter, HTTPException

from app.agents.finance import FinanceAgentService, FinanceAgentRequest, FinanceAgentResponse
from app.agents.marketing import MarketingAgentService, MarketingAgentRequest, MarketingAgentResponse
from app.agents.sales import SalesAgentService, SalesAgentRequest, SalesAgentResponse
from app.agents.hr import HRAgentService, HRAgentRequest, HRAgentResponse
from app.agents.operations import OperationsAgentService, OperationsAgentRequest, OperationsAgentResponse
from app.agents.legal import LegalAgentService, LegalAgentRequest, LegalAgentResponse
from app.agents.it import ITAgentService, ITAgentRequest, ITAgentResponse
from app.agents.business_analytics import AnalyticsAgentService, AnalyticsAgentRequest, AnalyticsAgentResponse
from app.agents.finance.service import LLMError

logger = logging.getLogger(__name__)

router = APIRouter()

finance_service = FinanceAgentService()
marketing_service = MarketingAgentService()
sales_service = SalesAgentService()
hr_service = HRAgentService()
operations_service = OperationsAgentService()
legal_service = LegalAgentService()
it_service = ITAgentService()
analytics_service = AnalyticsAgentService()


async def _persist_workspace_analysis(agent_id: str, scenario: str, response_dict: dict):
    """Persist a single workspace analysis to PostgreSQL (non-blocking)."""
    try:
        from app.mcp_hub.database import is_database_ready
        if not is_database_ready():
            return
        from app.mcp_hub.storage_service import StorageService
        storage = StorageService()
        session_id = str(uuid.uuid4())
        await storage.store_meeting(
            meeting_id=session_id,
            proposal=scenario,
            business_category=f"workspace_{agent_id}",
            title=f"[{agent_id.upper()}] {scenario[:100]}",
        )
        await storage.store_analysis(
            meeting_id=session_id,
            executive_role=agent_id,
            response=response_dict,
        )
    except Exception as e:
        logger.debug(f"Workspace persistence skipped: {e}")


@router.post("/finance", response_model=FinanceAgentResponse)
async def analyze_finance(request: FinanceAgentRequest) -> FinanceAgentResponse:
    """Submit a business proposal for Finance (CFO) analysis."""
    try:
        response = await finance_service.analyze(request)
        await _persist_workspace_analysis("finance", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/marketing", response_model=MarketingAgentResponse)
async def analyze_marketing(request: MarketingAgentRequest) -> MarketingAgentResponse:
    """Submit a business proposal for Marketing (CMO) analysis."""
    try:
        response = await marketing_service.analyze(request)
        await _persist_workspace_analysis("marketing", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/sales", response_model=SalesAgentResponse)
async def analyze_sales(request: SalesAgentRequest) -> SalesAgentResponse:
    """Submit a business proposal for Sales (CRO) analysis."""
    try:
        response = await sales_service.analyze(request)
        await _persist_workspace_analysis("sales", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/hr", response_model=HRAgentResponse)
async def analyze_hr(request: HRAgentRequest) -> HRAgentResponse:
    """Submit a business proposal for HR (CHRO) analysis."""
    try:
        response = await hr_service.analyze(request)
        await _persist_workspace_analysis("hr", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/operations", response_model=OperationsAgentResponse)
async def analyze_operations(request: OperationsAgentRequest) -> OperationsAgentResponse:
    """Submit a business proposal for Operations (COO) analysis."""
    try:
        response = await operations_service.analyze(request)
        await _persist_workspace_analysis("operations", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/legal", response_model=LegalAgentResponse)
async def analyze_legal(request: LegalAgentRequest) -> LegalAgentResponse:
    """Submit a business proposal for Legal (GC) analysis."""
    try:
        response = await legal_service.analyze(request)
        await _persist_workspace_analysis("legal", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/it", response_model=ITAgentResponse)
async def analyze_it(request: ITAgentRequest) -> ITAgentResponse:
    """Submit a business proposal for IT (CTO) analysis."""
    try:
        response = await it_service.analyze(request)
        await _persist_workspace_analysis("it", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/business_analytics", response_model=AnalyticsAgentResponse)
async def analyze_analytics(request: AnalyticsAgentRequest) -> AnalyticsAgentResponse:
    """Submit a business proposal for Business Analytics (CDO) analysis."""
    try:
        response = await analytics_service.analyze(request)
        await _persist_workspace_analysis("business_analytics", request.scenario, response.model_dump())
        return response
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


# --- Generic dynamic endpoint for ALL 20 agents ---

from pydantic import BaseModel, Field
from typing import Optional, Any

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

# Registry mapping agent_id to (service, request_class) for all 20 agents
AGENT_REGISTRY: dict = {
    "finance": (finance_service, FinanceAgentRequest),
    "marketing": (marketing_service, MarketingAgentRequest),
    "sales": (sales_service, SalesAgentRequest),
    "hr": (hr_service, HRAgentRequest),
    "operations": (operations_service, OperationsAgentRequest),
    "legal": (legal_service, LegalAgentRequest),
    "it": (it_service, ITAgentRequest),
    "business_analytics": (analytics_service, AnalyticsAgentRequest),
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


class GenericAgentRequest(BaseModel):
    """Generic request for any agent via the dynamic endpoint."""
    scenario: str = Field(..., min_length=20, description="Business proposal to analyze")
    context: Optional[str] = Field(default=None, description="Additional context")


@router.post("/analyze/{agent_id}")
async def analyze_generic(agent_id: str, request: GenericAgentRequest) -> dict[str, Any]:
    """Generic endpoint to invoke any registered agent by ID.

    Supports all 20 agents without requiring individual routes.
    """
    if agent_id not in AGENT_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_id}' not found. Available: {sorted(AGENT_REGISTRY.keys())}",
        )

    service, request_cls = AGENT_REGISTRY[agent_id]

    try:
        agent_request = request_cls(scenario=request.scenario, context=request.context)
        response = await service.analyze(agent_request)
        response_dict = response.model_dump()
        await _persist_workspace_analysis(agent_id, request.scenario, response_dict)
        return response_dict
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent '{agent_id}' error: {str(e)}")
