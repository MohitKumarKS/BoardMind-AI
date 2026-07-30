"""AI Governance & Ethics Officer module.

This module provides the complete AI Governance Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.ai_governance import AIGovernanceAgentService, AIGovernanceAgentRequest

    service = AIGovernanceAgentService()
    request = AIGovernanceAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    AIGovernanceAgentRequest,
    AIGovernanceAgentResponse,
    AIGovernanceDomainAssessment,
    Position,
    AIRiskLevel,
)
from .service import AIGovernanceAgentService, LLMError, LLMNotConfiguredError

__all__ = [
    "AIGovernanceAgentService",
    "AIGovernanceAgentRequest",
    "AIGovernanceAgentResponse",
    "AIGovernanceDomainAssessment",
    "Position",
    "AIRiskLevel",
    "LLMError",
    "LLMNotConfiguredError",
]
