"""Operations Agent response schema.

Pydantic models matching the Output Schema defined in the Operations Agent specification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class ExecutionComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CapacityImpact(str, Enum):
    WITHIN_CAPACITY = "within capacity"
    STRETCH = "stretch"
    OVERLOAD = "overload"


class OperationsDomainAssessment(BaseModel):
    """Structured operational impact analysis."""

    execution_complexity: ExecutionComplexity = Field(
        ..., description="Overall complexity of execution"
    )
    timeline_estimate: str = Field(
        ..., description="Realistic implementation timeline"
    )
    resource_requirements: str = Field(
        ..., description="People, tools, infrastructure needed"
    )
    capacity_impact: CapacityImpact = Field(
        ..., description="Effect on current operational capacity"
    )
    dependencies: list[str] = Field(
        ..., min_length=1, description="Critical dependencies identified"
    )


class OperationsAgentResponse(BaseModel):
    """Complete structured response from the Operations Agent."""

    agent_id: str = Field(default="operations")
    round: int = Field(default=1, ge=1, le=3)
    position: Position = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    domain_assessment: OperationsDomainAssessment = Field(...)
    summary: str = Field(..., min_length=10, max_length=300)
    rationale: str = Field(..., min_length=100)
    risks: list[str] = Field(..., min_length=1)
    conditions: list[str] = Field(default_factory=list)
    implementation_phases: list[str] = Field(
        ..., min_length=1, description="Suggested phasing for execution"
    )
    references_to: list[str] = Field(default_factory=list)

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        for risk in v:
            if len(risk) < 10:
                raise ValueError(f"Risk '{risk}' is too vague.")
        return v


class OperationsAgentRequest(BaseModel):
    """Input request for the Operations Agent."""

    scenario: str = Field(..., min_length=20)
    context: Optional[str] = Field(default=None)
