"""IT Agent response schema.

Pydantic models matching the Output Schema defined in the IT Agent specification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class Feasibility(str, Enum):
    STRAIGHTFORWARD = "straightforward"
    MODERATE = "moderate"
    COMPLEX = "complex"
    INFEASIBLE = "infeasible"


class SecurityRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InfrastructureNeeds(str, Enum):
    EXISTING = "existing"
    MINOR_ADDITIONS = "minor_additions"
    SIGNIFICANT_INVESTMENT = "significant_investment"


class IntegrationComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TechnicalDebtImpact(str, Enum):
    REDUCES = "reduces"
    NEUTRAL = "neutral"
    INCREASES = "increases"


class ITDomainAssessment(BaseModel):
    """Structured technical impact analysis."""

    feasibility: Feasibility = Field(
        ..., description="Technical feasibility assessment"
    )
    security_risk: SecurityRisk = Field(
        ..., description="Security risk classification"
    )
    infrastructure_needs: InfrastructureNeeds = Field(
        ..., description="Infrastructure requirements"
    )
    integration_complexity: IntegrationComplexity = Field(
        ..., description="Complexity of integrating with existing systems"
    )
    technical_debt_impact: TechnicalDebtImpact = Field(
        ..., description="Effect on technical debt"
    )


class ITAgentResponse(BaseModel):
    """Complete structured response from the IT Agent."""

    agent_id: str = Field(default="it")
    round: int = Field(default=1, ge=1, le=3)
    position: Position = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    domain_assessment: ITDomainAssessment = Field(...)
    summary: str = Field(..., min_length=10, max_length=300)
    rationale: str = Field(..., min_length=100)
    risks: list[str] = Field(..., min_length=1)
    conditions: list[str] = Field(default_factory=list)
    effort_estimate: str = Field(
        ..., min_length=10, description="High-level effort and timeline range"
    )
    references_to: list[str] = Field(default_factory=list)

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        for risk in v:
            if len(risk) < 10:
                raise ValueError(f"Risk '{risk}' is too vague.")
        return v


class ITAgentRequest(BaseModel):
    """Input request for the IT Agent."""

    scenario: str = Field(..., min_length=20)
    context: Optional[str] = Field(default=None)
