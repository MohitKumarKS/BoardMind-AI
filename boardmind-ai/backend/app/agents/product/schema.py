"""Product Agent response schema.

Pydantic models matching the Output Schema defined in the Product Agent specification.
These models define the contract for structured output from the Chief Product Officer Agent.
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


class Feasibility(str, Enum):
    """Product feasibility classification."""

    STRAIGHTFORWARD = "straightforward"
    MODERATE = "moderate"
    COMPLEX = "complex"
    INFEASIBLE = "infeasible"


class ProductDomainAssessment(BaseModel):
    """Structured product impact analysis.

    Every field must contain a substantive product assessment with
    clear reasoning tied to user needs and product-market dynamics.
    """

    product_market_fit: str = Field(
        ...,
        description="Demand validation and user need assessment",
        examples=["Strong PMF signals: 40% of surveyed users cite this as top-3 unmet need; 3 competitors validate demand"],
    )
    roadmap_impact: str = Field(
        ...,
        description="Effect on current product roadmap and planned deliverables",
        examples=["Displaces Q3 feature work (2 engineers, 6 weeks); delays loyalty program by one quarter"],
    )
    user_experience: str = Field(
        ...,
        description="UX implications and user journey impact assessment",
        examples=["Reduces onboarding steps from 7 to 3; expected 25% improvement in activation rate"],
    )
    build_vs_buy: str = Field(
        ...,
        description="Make, buy, or partner analysis for this capability",
        examples=["Build recommended: core differentiator, no adequate vendor solution exists at our scale requirements"],
    )
    feasibility: Feasibility = Field(
        ...,
        description="Overall product feasibility classification",
    )


class ProductAgentResponse(BaseModel):
    """Complete structured response from the Product Agent.

    This schema enforces the output contract defined in the Product Agent
    specification. All fields are required to ensure comprehensive analysis.
    """

    agent_id: str = Field(
        default="product",
        description="Unique identifier for the Product department agent",
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
    domain_assessment: ProductDomainAssessment = Field(
        ...,
        description="Structured product impact analysis",
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
        description="Detailed product reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific, actionable product risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for product support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended product KPIs to monitor",
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


class ProductAgentRequest(BaseModel):
    """Input request for the Product Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering adding a real-time collaboration feature to our "
            "project management tool to compete with Notion and Monday.com."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
