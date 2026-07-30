"""Investor Relations Officer module.

This module provides the complete Investor Relations Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.investor_relations import InvestorRelationsAgentService, InvestorRelationsAgentRequest

    service = InvestorRelationsAgentService()
    request = InvestorRelationsAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    InvestorRelationsAgentRequest,
    InvestorRelationsAgentResponse,
    InvestorRelationsDomainAssessment,
    Position,
    InvestorSentiment,
)
from .service import InvestorRelationsAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "InvestorRelationsAgentService",
    "InvestorRelationsAgentRequest",
    "InvestorRelationsAgentResponse",
    "InvestorRelationsDomainAssessment",
    "Position",
    "InvestorSentiment",
    "LLMError",
    "LLMNotConfiguredError",
]
