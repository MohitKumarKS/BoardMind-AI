"""Chief Risk Officer Agent module.

This module provides the complete Risk Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.risk import RiskAgentService, RiskAgentRequest

    service = RiskAgentService()
    request = RiskAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    RiskAgentRequest,
    RiskAgentResponse,
    RiskDomainAssessment,
    Position,
    RiskLevel,
)
from .service import RiskAgentService

__all__ = [
    "RiskAgentService",
    "RiskAgentRequest",
    "RiskAgentResponse",
    "RiskDomainAssessment",
    "Position",
    "RiskLevel",
]
