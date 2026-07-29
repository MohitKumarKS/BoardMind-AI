"""Finance Agent module.

This module provides the complete Finance Agent implementation for
the BoardMind AI platform. It serves as the reference implementation
for all future department agents.

Usage:
    from app.agents.finance import FinanceAgentService, FinanceAgentRequest

    service = FinanceAgentService()
    request = FinanceAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    FinanceAgentRequest,
    FinanceAgentResponse,
    FinanceDomainAssessment,
    Position,
    RiskLevel,
)
from .service import FinanceAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "FinanceAgentService",
    "FinanceAgentRequest",
    "FinanceAgentResponse",
    "FinanceDomainAssessment",
    "Position",
    "RiskLevel",
    "LLMError",
    "LLMNotConfiguredError",
]
