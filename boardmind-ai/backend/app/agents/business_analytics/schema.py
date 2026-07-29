"""Business Analytics Agent response schema.

Pydantic models matching the Output Schema defined in the Business Analytics Agent specification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class EvidenceStrength(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    INSUFFICIENT = "insufficient"


class DataAvailability(str, Enum):
    AVAILABLE = "available"
    PARTIALLY_AVAILABLE = "partially_available"
    NOT_AVAILABLE = "not_available"


class ProjectionConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AnalyticsDomainAssessment(BaseModel):
    """Structured analytics and evidence assessment."""

    evidence_strength: EvidenceStrength = Field(
        ..., description="Strength of evidence supporting the proposal"
    )
    data_availability: DataAvailability = Field(
        ..., description="Availability of data needed for decision"
    )
    projection_confidence: ProjectionConfidence = Field(
        ..., description="Confidence in projections made by the proposal"
    )
    key_metrics: list[str] = Field(
        ..., min_length=1, description="Key metrics to track"
    )
    benchmarks: list[str] = Field(
        ..., min_length=1, description="Relevant industry benchmarks"
    )


class AnalyticsAgentResponse(BaseModel):
    """Complete structured response from the Business Analytics Agent."""

    agent_id: str = Field(default="business_analytics")
    round: int = Field(default=1, ge=1, le=3)
    position: Position = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    domain_assessment: AnalyticsDomainAssessment = Field(...)
    summary: str = Field(..., min_length=10, max_length=300)
    rationale: str = Field(..., min_length=100)
    risks: list[str] = Field(..., min_length=1)
    conditions: list[str] = Field(default_factory=list)
    measurement_plan: str = Field(
        ..., min_length=20, description="How to define and track success"
    )
    references_to: list[str] = Field(default_factory=list)

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        for risk in v:
            if len(risk) < 10:
                raise ValueError(f"Risk '{risk}' is too vague.")
        return v


class AnalyticsAgentRequest(BaseModel):
    """Input request for the Business Analytics Agent."""

    scenario: str = Field(..., min_length=20)
    context: Optional[str] = Field(default=None)
