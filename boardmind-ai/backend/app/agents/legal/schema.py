"""Legal Agent response schema.

Pydantic models matching the Output Schema defined in the Legal Agent specification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non-compliant"
    REQUIRES_REVIEW = "requires_review"


class LegalRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IPImplications(str, Enum):
    NONE = "none"
    MINOR = "minor"
    SIGNIFICANT = "significant"


class LegalDomainAssessment(BaseModel):
    """Structured legal impact analysis."""

    compliance_status: ComplianceStatus = Field(
        ..., description="Current compliance posture for the proposal"
    )
    risk_level: LegalRiskLevel = Field(
        ..., description="Overall legal risk classification"
    )
    liability_exposure: str = Field(
        ..., description="Estimated liability exposure description"
    )
    regulatory_bodies: list[str] = Field(
        ..., min_length=1, description="Relevant regulatory bodies or frameworks"
    )
    ip_implications: IPImplications = Field(
        ..., description="Intellectual property implications"
    )


class LegalAgentResponse(BaseModel):
    """Complete structured response from the Legal Agent."""

    agent_id: str = Field(default="legal")
    round: int = Field(default=1, ge=1, le=3)
    position: Position = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    domain_assessment: LegalDomainAssessment = Field(...)
    summary: str = Field(..., min_length=10, max_length=300)
    rationale: str = Field(..., min_length=100)
    risks: list[str] = Field(..., min_length=1)
    conditions: list[str] = Field(default_factory=list)
    required_safeguards: list[str] = Field(
        ..., min_length=1, description="Legal protections needed before proceeding"
    )
    references_to: list[str] = Field(default_factory=list)

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        for risk in v:
            if len(risk) < 10:
                raise ValueError(f"Risk '{risk}' is too vague.")
        return v


class LegalAgentRequest(BaseModel):
    """Input request for the Legal Agent."""

    scenario: str = Field(..., min_length=20)
    context: Optional[str] = Field(default=None)
