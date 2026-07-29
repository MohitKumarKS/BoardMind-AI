"""Sales Agent response schema.

Pydantic models matching the Output Schema defined in the Sales Agent specification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class PipelineImpact(str, Enum):
    NEW_PIPELINE = "new pipeline"
    ACCELERATION = "acceleration"
    DISRUPTION = "disruption"


class DealCycleEffect(str, Enum):
    SHORTER = "shorter"
    LONGER = "longer"
    UNCHANGED = "unchanged"


class CompetitiveEffect(str, Enum):
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"
    NEUTRAL = "neutral"


class SalesDomainAssessment(BaseModel):
    """Structured revenue impact analysis."""

    revenue_upside: str = Field(
        ..., description="Projected additional revenue with timeline"
    )
    revenue_risk: str = Field(
        ..., description="Potential revenue at risk"
    )
    pipeline_impact: PipelineImpact = Field(
        ..., description="Effect on sales pipeline"
    )
    deal_cycle_effect: DealCycleEffect = Field(
        ..., description="Effect on deal closure timeline"
    )
    competitive_effect: CompetitiveEffect = Field(
        ..., description="Effect on competitive positioning in deals"
    )


class SalesAgentResponse(BaseModel):
    """Complete structured response from the Sales Agent."""

    agent_id: str = Field(default="sales")
    round: int = Field(default=1, ge=1, le=3)
    position: Position = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    domain_assessment: SalesDomainAssessment = Field(...)
    summary: str = Field(..., min_length=10, max_length=300)
    rationale: str = Field(..., min_length=100)
    risks: list[str] = Field(..., min_length=1)
    conditions: list[str] = Field(default_factory=list)
    customer_impact: str = Field(
        ..., min_length=20, description="How key accounts would be affected"
    )
    references_to: list[str] = Field(default_factory=list)

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        for risk in v:
            if len(risk) < 10:
                raise ValueError(f"Risk '{risk}' is too vague.")
        return v


class SalesAgentRequest(BaseModel):
    """Input request for the Sales Agent."""

    scenario: str = Field(..., min_length=20)
    context: Optional[str] = Field(default=None)
