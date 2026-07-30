"""Chief Risk Officer Agent response schema.

Pydantic models for the Chief Risk Officer agent.
Focuses on enterprise risk management, risk quantification,
risk appetite, and scenario analysis.
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
    """Enterprise risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskDomainAssessment(BaseModel):
    """Structured risk assessment from the CRO perspective.

    Every field must contain a substantive risk analysis — generic
    responses violate the Risk Agent's design constraints.
    """

    risk_exposure: str = Field(
        ...,
        description="Quantified risk exposure (expected loss, VaR, or range)",
        examples=["Estimated maximum exposure of $2.4M (95% confidence interval), with expected loss of $800K based on probability-weighted scenario analysis"],
    )
    probability_assessment: str = Field(
        ...,
        description="Likelihood of adverse outcomes with supporting reasoning",
        examples=["35-45% probability of material adverse outcome based on historical analogs and Monte Carlo simulation of key variables"],
    )
    mitigation_strategy: str = Field(
        ...,
        description="Risk mitigation recommendations with effectiveness estimates",
        examples=["Phased implementation reduces maximum exposure from $2.4M to $900K. Transfer residual risk via $500K insurance policy. Accept remaining $400K within risk appetite."],
    )
    residual_risk: str = Field(
        ...,
        description="Remaining risk after proposed controls are applied",
        examples=["Post-mitigation residual risk: $400K expected loss (within board-approved risk appetite of $600K per initiative). Residual probability: 12-18%."],
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Overall enterprise risk classification",
    )


class RiskAgentResponse(BaseModel):
    """Complete structured response from the Risk Agent.

    This schema enforces the output contract for the CRO agent.
    All fields are required to ensure comprehensive risk analysis.
    """

    agent_id: str = Field(
        default="risk",
        description="Unique identifier for the Risk agent",
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
    domain_assessment: RiskDomainAssessment = Field(
        ...,
        description="Structured enterprise risk assessment",
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
        description="Detailed risk reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific enterprise risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Risk management requirements for support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended risk KPIs to monitor",
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


class RiskAgentRequest(BaseModel):
    """Input request for the Risk Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering expanding into a new market segment with "
            "uncertain regulatory environment and limited historical data."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
