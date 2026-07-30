"""ESG & Sustainability Officer module.

This module provides the complete ESG Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.esg import ESGAgentService, ESGAgentRequest

    service = ESGAgentService()
    request = ESGAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    ESGAgentRequest,
    ESGAgentResponse,
    ESGDomainAssessment,
    Position,
    ESGRiskLevel,
)
from .service import ESGAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "ESGAgentService",
    "ESGAgentRequest",
    "ESGAgentResponse",
    "ESGDomainAssessment",
    "Position",
    "ESGRiskLevel",
    "LLMError",
    "LLMNotConfiguredError",
]
