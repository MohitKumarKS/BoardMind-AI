"""CEO Agent module.

This module provides the complete CEO Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.ceo import CEOAgentService, CEOAgentRequest

    service = CEOAgentService()
    request = CEOAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    CEOAgentRequest,
    CEOAgentResponse,
    CEODomainAssessment,
    Position,
    RiskLevel,
)
from .service import CEOAgentService

__all__ = [
    "CEOAgentService",
    "CEOAgentRequest",
    "CEOAgentResponse",
    "CEODomainAssessment",
    "Position",
    "RiskLevel",
]
