"""Legal Agent module."""

from .schema import (
    LegalAgentRequest,
    LegalAgentResponse,
    LegalDomainAssessment,
    Position,
    ComplianceStatus,
    LegalRiskLevel,
    IPImplications,
)
from .service import LegalAgentService

__all__ = [
    "LegalAgentService",
    "LegalAgentRequest",
    "LegalAgentResponse",
    "LegalDomainAssessment",
    "Position",
    "ComplianceStatus",
    "LegalRiskLevel",
    "IPImplications",
]
