"""Compliance Officer Agent module.

This module provides the complete Compliance Agent implementation for
the BoardMind AI platform.

Usage:
    from app.agents.compliance import ComplianceAgentService, ComplianceAgentRequest

    service = ComplianceAgentService()
    request = ComplianceAgentRequest(scenario="Your business proposal here")
    response = await service.analyze(request)
"""

from .schema import (
    ComplianceAgentRequest,
    ComplianceAgentResponse,
    ComplianceDomainAssessment,
    Position,
    ComplianceStatus,
)
from .service import ComplianceAgentService

__all__ = [
    "ComplianceAgentService",
    "ComplianceAgentRequest",
    "ComplianceAgentResponse",
    "ComplianceDomainAssessment",
    "Position",
    "ComplianceStatus",
]
