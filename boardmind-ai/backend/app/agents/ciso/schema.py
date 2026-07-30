"""CISO Agent response schema.

Pydantic models for the Chief Information Security Officer agent.
Focuses on cybersecurity, threat assessment, data protection,
and security compliance.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    """The agent's stance on the business proposal."""

    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class SecurityRisk(str, Enum):
    """Security risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CISODomainAssessment(BaseModel):
    """Structured security assessment from the CISO perspective.

    Every field must contain a substantive security analysis — generic
    responses violate the CISO Agent's design constraints.
    """

    threat_exposure: str = Field(
        ...,
        description="New attack surface or threats introduced by the proposal",
    )
    data_protection_impact: str = Field(
        ...,
        description="Impact on sensitive data handling and privacy",
    )
    compliance_posture: str = Field(
        ...,
        description="Security compliance status (SOC2, ISO27001, etc.)",
    )
    security_investment: str = Field(
        ...,
        description="Security controls and costs needed",
    )
    security_risk: SecurityRisk = Field(
        ...,
        description="Overall security risk classification",
    )


class CISOAgentResponse(BaseModel):
    """Complete structured response from the CISO Agent.

    This schema enforces the output contract for the CISO agent.
    All fields are required to ensure comprehensive security analysis.
    """

    agent_id: str = Field(
        default="ciso",
        description="Unique identifier for the CISO agent",
    )
    round: int = Field(
        default=1,
        ge=1,
        le=3,
        description="Deliberation round (1 for Department Workspace mode)",
    )
    position: Position = Field(
        ...,
        description="The agent's stance on the proposal",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Certainty in position (0.0 = no confidence, 1.0 = absolute certainty)",
    )
    domain_assessment: CISODomainAssessment = Field(
        ...,
        description="Structured security assessment",
    )
    summary: str = Field(
        ...,
        min_length=10,
        max_length=300,
        description="One-sentence position statement",
    )
    rationale: str = Field(
        ...,
        min_length=100,
        description="Detailed security reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific security risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Security requirements that must be met for support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended security KPIs to monitor",
    )
    references_to: list[str] = Field(
        default_factory=list,
        description="Agent IDs referenced in reasoning (empty in Department Workspace mode)",
    )

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        """Ensure risks are specific and actionable, not generic warnings."""
        for risk in v:
            if len(risk) < 10:
                raise ValueError(
                    f"Risk '{risk}' is too vague. Risks must be specific and actionable."
                )
        return v

    @field_validator("metrics_to_track")
    @classmethod
    def metrics_must_be_measurable(cls, v: list[str]) -> list[str]:
        """Ensure metrics are concrete and measurable."""
        for metric in v:
            if len(metric) < 5:
                raise ValueError(
                    f"Metric '{metric}' is too vague. Metrics must be measurable."
                )
        return v


class CISOAgentRequest(BaseModel):
    """Input request for the CISO Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering migrating our customer data to a new cloud "
            "provider to reduce costs and improve scalability."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
