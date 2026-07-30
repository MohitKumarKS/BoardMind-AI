"""CEO Agent response schema.

Pydantic models for the Chief Executive Officer agent.
Focuses on strategic vision, corporate direction, stakeholder alignment,
and executive decision-making.
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
    """Strategic risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CEODomainAssessment(BaseModel):
    """Structured strategic assessment from the CEO perspective.

    Every field must contain a substantive strategic analysis — generic
    responses violate the CEO Agent's design constraints.
    """

    strategic_alignment: str = Field(
        ...,
        description="How the proposal aligns with company vision and strategic priorities",
        examples=["Strongly aligned with our 3-year vision of becoming the market leader in AI-driven analytics — directly accelerates Goal #2 (expand enterprise segment by 40%)"],
    )
    stakeholder_impact: str = Field(
        ...,
        description="Impact on key stakeholders including shareholders, employees, customers, and partners",
        examples=["Positive for shareholders (projected 25% value increase), moderate disruption for 30% of engineering staff requiring reskilling, strengthens customer trust through improved capabilities"],
    )
    competitive_positioning: str = Field(
        ...,
        description="Effect on market position relative to competitors",
        examples=["Moves us from #3 to potential #2 in the enterprise segment within 18 months, creates 12-month competitive moat through proprietary data integration"],
    )
    execution_priority: str = Field(
        ...,
        description="Urgency and resource priority relative to other initiatives",
        examples=["High priority — recommend moving to P1 status, reallocating 20% of Q3 discretionary budget. Delay beyond Q2 risks competitor first-mover advantage."],
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Overall strategic risk classification",
    )


class CEOAgentResponse(BaseModel):
    """Complete structured response from the CEO Agent.

    This schema enforces the output contract for the CEO agent.
    All fields are required to ensure comprehensive strategic analysis.
    """

    agent_id: str = Field(
        default="ceo",
        description="Unique identifier for the CEO agent",
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
    domain_assessment: CEODomainAssessment = Field(
        ...,
        description="Structured strategic assessment",
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
        description="Detailed strategic reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific strategic risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended strategic KPIs to monitor",
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


class CEOAgentRequest(BaseModel):
    """Input request for the CEO Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering a strategic pivot from B2C to B2B enterprise "
            "to capture higher contract values and reduce churn."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
