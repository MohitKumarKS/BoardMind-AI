"""Finance Agent response schema.

Pydantic models matching the Output Schema defined in the Finance Agent specification.
These models serve as the contract for structured output from the Finance Agent
and will be reused as the pattern for all future department agents.
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


class RiskLevel(str, Enum):
    """Financial risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FinanceDomainAssessment(BaseModel):
    """Structured financial impact analysis.

    Every field must contain a quantified assessment — qualitative-only
    responses violate the Finance Agent's design constraints.
    """

    revenue_impact: str = Field(
        ...,
        description="Estimated revenue change with quantification and timeframe",
        examples=["Projected +$2.4M annual revenue by Year 2, assuming 15% market penetration"],
    )
    cost_impact: str = Field(
        ...,
        description="Estimated cost change including direct and indirect costs",
        examples=["Initial investment of $800K (Year 1), ongoing $200K/year operational costs"],
    )
    roi_estimate: str = Field(
        ...,
        description="Projected ROI with clearly stated assumptions",
        examples=["Expected 180% ROI over 3 years, assuming 20% YoY growth and 70% gross margin"],
    )
    payback_period: str = Field(
        ...,
        description="Time to recoup the initial investment",
        examples=["14-18 months at projected adoption rates"],
    )
    risk_level: RiskLevel = Field(
        default=RiskLevel.MEDIUM,
        description="Overall financial risk classification",
    )


class FinanceAgentResponse(BaseModel):
    """Complete structured response from the Finance Agent.

    This schema enforces the output contract defined in the Finance Agent
    specification. All fields are required to ensure comprehensive analysis.
    """

    agent_id: str = Field(
        default="finance",
        description="Unique identifier for the Finance department agent",
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
    domain_assessment: FinanceDomainAssessment = Field(
        ...,
        description="Structured financial impact analysis",
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
        description="Detailed financial reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific, actionable financial risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Measurable requirements that must be met for support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended financial KPIs to monitor",
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


class FinanceAgentRequest(BaseModel):
    """Input request for the Finance Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering launching a new SaaS product targeting mid-market "
            "companies with a $50K development budget and 6-month timeline."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
