"""Customer Success Agent module.

This module provides the complete Customer Success Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.customer_success import CustomerSuccessAgentService, CustomerSuccessAgentRequest

    service = CustomerSuccessAgentService()
    request = CustomerSuccessAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    CustomerSuccessAgentRequest,
    CustomerSuccessAgentResponse,
    CustomerSuccessDomainAssessment,
    Position,
    CustomerRisk,
)
from .service import CustomerSuccessAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "CustomerSuccessAgentService",
    "CustomerSuccessAgentRequest",
    "CustomerSuccessAgentResponse",
    "CustomerSuccessDomainAssessment",
    "Position",
    "CustomerRisk",
    "LLMError",
    "LLMNotConfiguredError",
]
