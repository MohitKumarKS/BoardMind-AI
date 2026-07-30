"""Product Agent module.

This module provides the complete Product Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.product import ProductAgentService, ProductAgentRequest

    service = ProductAgentService()
    request = ProductAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    ProductAgentRequest,
    ProductAgentResponse,
    ProductDomainAssessment,
    Position,
    Feasibility,
)
from .service import ProductAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "ProductAgentService",
    "ProductAgentRequest",
    "ProductAgentResponse",
    "ProductDomainAssessment",
    "Position",
    "Feasibility",
    "LLMError",
    "LLMNotConfiguredError",
]
