"""Department Workspace API routes.

Provides endpoints for single-agent analysis in Department Workspace mode.
Each agent operates independently — no orchestration or consensus.
"""

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

router = APIRouter()

finance_service = FinanceAgentService()
marketing_service = MarketingAgentService()
sales_service = SalesAgentService()
hr_service = HRAgentService()
operations_service = OperationsAgentService()
legal_service = LegalAgentService()
it_service = ITAgentService()
analytics_service = AnalyticsAgentService()


@router.post("/finance", response_model=FinanceAgentResponse)
async def analyze_finance(request: FinanceAgentRequest) -> FinanceAgentResponse:
    """Submit a business proposal for Finance (CFO) analysis."""
    try:
        return await finance_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/marketing", response_model=MarketingAgentResponse)
async def analyze_marketing(request: MarketingAgentRequest) -> MarketingAgentResponse:
    """Submit a business proposal for Marketing (CMO) analysis."""
    try:
        return await marketing_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/sales", response_model=SalesAgentResponse)
async def analyze_sales(request: SalesAgentRequest) -> SalesAgentResponse:
    """Submit a business proposal for Sales (CRO) analysis."""
    try:
        return await sales_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/hr", response_model=HRAgentResponse)
async def analyze_hr(request: HRAgentRequest) -> HRAgentResponse:
    """Submit a business proposal for HR (CHRO) analysis."""
    try:
        return await hr_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/operations", response_model=OperationsAgentResponse)
async def analyze_operations(request: OperationsAgentRequest) -> OperationsAgentResponse:
    """Submit a business proposal for Operations (COO) analysis."""
    try:
        return await operations_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/legal", response_model=LegalAgentResponse)
async def analyze_legal(request: LegalAgentRequest) -> LegalAgentResponse:
    """Submit a business proposal for Legal (GC) analysis."""
    try:
        return await legal_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/it", response_model=ITAgentResponse)
async def analyze_it(request: ITAgentRequest) -> ITAgentResponse:
    """Submit a business proposal for IT (CTO) analysis."""
    try:
        return await it_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/business_analytics", response_model=AnalyticsAgentResponse)
async def analyze_analytics(request: AnalyticsAgentRequest) -> AnalyticsAgentResponse:
    """Submit a business proposal for Business Analytics (CDO) analysis."""
    try:
        return await analytics_service.analyze(request)
    except LLMError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
