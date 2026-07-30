"""Chief Innovation Officer module.

This module provides the complete Innovation Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.innovation import InnovationAgentService, InnovationAgentRequest

    service = InnovationAgentService()
    request = InnovationAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    InnovationAgentRequest,
    InnovationAgentResponse,
    InnovationDomainAssessment,
    Position,
    InnovationRiskLevel,
)
from .service import InnovationAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "InnovationAgentService",
    "InnovationAgentRequest",
    "InnovationAgentResponse",
    "InnovationDomainAssessment",
    "Position",
    "InnovationRiskLevel",
    "LLMError",
    "LLMNotConfiguredError",
]
