"""Customer Success Agent response schema.

Pydantic models matching the Output Schema defined in the Customer Success Agent specification.
These models define the contract for structured output from the Chief Customer Officer Agent.
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


class CustomerRisk(str, Enum):
    """Customer risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CustomerSuccessDomainAssessment(BaseModel):
    """Structured customer success impact analysis.

    Every field must contain a substantive customer-centric assessment with
    clear reasoning tied to retention, satisfaction, and lifecycle management.
    """

    customer_impact: str = Field(
        ...,
        description="Impact assessment on existing customer base",
        examples=["Affects 60% of enterprise customers directly; expected 15% improvement in health scores for impacted cohort"],
    )
    retention_risk: str = Field(
        ...,
        description="Churn risk assessment and mitigation analysis",
        examples=["Moderate churn risk: 8% of at-risk accounts cite this capability gap; addressing it reduces projected churn by 3-5%"],
    )
    satisfaction_forecast: str = Field(
        ...,
        description="Expected NPS/CSAT effect and satisfaction trajectory",
        examples=["Expected NPS improvement of +8 points within 6 months; CSAT for affected workflows projected to rise from 3.6 to 4.2"],
    )
    support_requirements: str = Field(
        ...,
        description="Customer support needs and resource implications",
        examples=["Estimated 200 additional support tickets in first month; requires 2 dedicated CSMs for onboarding wave"],
    )
    customer_risk: CustomerRisk = Field(
        default=CustomerRisk.MEDIUM,
        description="Overall customer risk classification",
    )


class CustomerSuccessAgentResponse(BaseModel):
    """Complete structured response from the Customer Success Agent.

    This schema enforces the output contract defined in the Customer Success Agent
    specification. All fields are required to ensure comprehensive analysis.
    """

    agent_id: str = Field(
        default="customer_success",
        description="Unique identifier for the Customer Success department agent",
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
    domain_assessment: CustomerSuccessDomainAssessment = Field(
        ...,
        description="Structured customer success impact analysis",
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
        description="Detailed customer success reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific, actionable customer success risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for customer success support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended customer success KPIs to monitor",
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
            if len(metric) < 3:
                raise ValueError(
                    f"Metric '{metric}' is too vague. Metrics must be measurable."
                )
        return v


class CustomerSuccessAgentRequest(BaseModel):
    """Input request for the Customer Success Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering migrating all customers from our legacy platform "
            "to the new v3 architecture over 6 months with mandatory cutover."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
