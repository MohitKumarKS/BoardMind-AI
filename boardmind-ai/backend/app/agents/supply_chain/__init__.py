"""Supply Chain Agent module.

This module provides the complete Supply Chain Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.supply_chain import SupplyChainAgentService, SupplyChainAgentRequest

    service = SupplyChainAgentService()
    request = SupplyChainAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    SupplyChainAgentRequest,
    SupplyChainAgentResponse,
    SupplyChainDomainAssessment,
    Position,
    OperationalRisk,
)
from .service import SupplyChainAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "SupplyChainAgentService",
    "SupplyChainAgentRequest",
    "SupplyChainAgentResponse",
    "SupplyChainDomainAssessment",
    "Position",
    "OperationalRisk",
    "LLMError",
    "LLMNotConfiguredError",
]
