"""Marketing Agent response schema.

Pydantic models matching the Output Schema defined in the Marketing Agent specification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class BrandImpact(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class CompetitivePosition(str, Enum):
    STRENGTHENED = "strengthened"
    WEAKENED = "weakened"
    UNCHANGED = "unchanged"


class GoToMarketComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MarketingDomainAssessment(BaseModel):
    """Structured market impact analysis."""

    market_opportunity: str = Field(
        ...,
        description="TAM/SAM/SOM estimates or qualitative market sizing",
    )
    brand_impact: BrandImpact = Field(
        ...,
        description="Overall brand positioning effect",
    )
    competitive_position: CompetitivePosition = Field(
        ...,
        description="Effect on competitive standing",
    )
    customer_segments_affected: list[str] = Field(
        ...,
        min_length=1,
        description="Customer segments impacted by this proposal",
    )
    go_to_market_complexity: GoToMarketComplexity = Field(
        ...,
        description="Complexity of bringing this to market",
    )


class MarketingAgentResponse(BaseModel):
    """Complete structured response from the Marketing Agent."""

    agent_id: str = Field(default="marketing")
    round: int = Field(default=1, ge=1, le=3)
    position: Position = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    domain_assessment: MarketingDomainAssessment = Field(...)
    summary: str = Field(..., min_length=10, max_length=300)
    rationale: str = Field(..., min_length=100)
    risks: list[str] = Field(..., min_length=1)
    conditions: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(..., min_length=1)
    references_to: list[str] = Field(default_factory=list)

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        for risk in v:
            if len(risk) < 10:
                raise ValueError(f"Risk '{risk}' is too vague.")
        return v

    @field_validator("recommended_actions")
    @classmethod
    def actions_must_be_actionable(cls, v: list[str]) -> list[str]:
        for action in v:
            if len(action) < 10:
                raise ValueError(f"Action '{action}' is too vague.")
        return v


class MarketingAgentRequest(BaseModel):
    """Input request for the Marketing Agent."""

    scenario: str = Field(..., min_length=20)
    context: Optional[str] = Field(default=None)
