"""Investor Relations Officer response schema.

Pydantic models matching the Output Schema for the Investor Relations Agent.
These models enforce structured output for shareholder communication, market
perception, analyst relations, and earnings impact analysis.
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


class InvestorSentiment(str, Enum):
    """Investor sentiment classification."""

    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class InvestorRelationsDomainAssessment(BaseModel):
    """Structured investor relations impact analysis.

    Every field must contain a substantive assessment covering market
    perception, earnings impact, shareholder value, and communication strategy.
    """

    market_perception: str = Field(
        ...,
        description="How investors and analysts will perceive this decision",
        examples=["Analysts likely to view positively: aligns with stated growth strategy and consensus expectations for market expansion"],
    )
    earnings_impact: str = Field(
        ...,
        description="Effect on EPS, guidance, and quarterly results",
        examples=["Near-term EPS dilution of $0.05-0.08 for 2 quarters; accretive by Q3 FY25 if execution targets met"],
    )
    shareholder_value: str = Field(
        ...,
        description="Long-term shareholder value creation or destruction",
        examples=["Projected 15-20% long-term value creation through TAM expansion; risk of 5-8% erosion if execution falters"],
    )
    communication_strategy: str = Field(
        ...,
        description="Recommended messaging to investor community",
        examples=["Frame as strategic investment in TAM expansion; pre-brief top 10 institutional holders; include in next earnings guidance update"],
    )
    investor_sentiment: InvestorSentiment = Field(
        ...,
        description="Predicted investor sentiment classification",
    )

    @field_validator("market_perception")
    @classmethod
    def perception_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Market perception assessment must be detailed and specific.")
        return v

    @field_validator("earnings_impact")
    @classmethod
    def earnings_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Earnings impact assessment must be detailed and specific.")
        return v

    @field_validator("shareholder_value")
    @classmethod
    def value_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Shareholder value assessment must be detailed and specific.")
        return v

    @field_validator("communication_strategy")
    @classmethod
    def comms_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Communication strategy must be detailed and specific.")
        return v


class InvestorRelationsAgentResponse(BaseModel):
    """Complete structured response from the Investor Relations Officer.

    This schema enforces the output contract for comprehensive investor
    relations analysis covering market perception, earnings impact, and
    shareholder communication.
    """

    agent_id: str = Field(
        default="investor_relations",
        description="Unique identifier for the Investor Relations department agent",
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
    domain_assessment: InvestorRelationsDomainAssessment = Field(
        ...,
        description="Structured investor relations impact analysis",
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
        description="Detailed investor relations reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific investor relations and market perception risks",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements for favorable market communication",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended investor-facing KPIs to monitor",
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


class InvestorRelationsAgentRequest(BaseModel):
    """Input request for the Investor Relations Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze from an investor relations perspective",
        examples=[
            "We are considering a major acquisition that would double our revenue "
            "but require issuing $500M in new shares, diluting existing shareholders by 15%."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
