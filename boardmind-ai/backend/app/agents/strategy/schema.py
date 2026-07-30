"""Strategy Agent response schema.

Pydantic models matching the Output Schema defined in the Strategy Agent specification.
These models define the contract for structured output from the Chief Strategy Officer Agent.
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


class StrategicPriority(str, Enum):
    """Strategic priority classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StrategyDomainAssessment(BaseModel):
    """Structured strategic impact analysis.

    Every field must contain a substantive strategic assessment with
    clear reasoning tied to market dynamics and competitive positioning.
    """

    market_opportunity: str = Field(
        ...,
        description="Addressable market size and growth potential assessment",
        examples=["TAM of $4.2B growing at 18% CAGR; SAM of $800M with realistic SOM of $120M within 3 years"],
    )
    competitive_advantage: str = Field(
        ...,
        description="Differentiation analysis and sustainable moat evaluation",
        examples=["Strong IP moat via proprietary ML models; 18-month first-mover advantage in vertical AI segment"],
    )
    strategic_fit: str = Field(
        ...,
        description="Alignment with current corporate strategic plan and vision",
        examples=["Directly supports pillar 2 of our 3-year plan: 'Expand into adjacent verticals via AI-first products'"],
    )
    execution_complexity: str = Field(
        ...,
        description="Strategic execution difficulty and organizational readiness",
        examples=["High complexity — requires new capabilities in data partnerships and regulatory navigation"],
    )
    strategic_priority: StrategicPriority = Field(
        ...,
        description="Overall strategic priority classification",
    )


class StrategyAgentResponse(BaseModel):
    """Complete structured response from the Strategy Agent.

    This schema enforces the output contract defined in the Strategy Agent
    specification. All fields are required to ensure comprehensive analysis.
    """

    agent_id: str = Field(
        default="strategy",
        description="Unique identifier for the Strategy department agent",
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
    domain_assessment: StrategyDomainAssessment = Field(
        ...,
        description="Structured strategic impact analysis",
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
        description="Specific, actionable strategic risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for strategic support",
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


class StrategyAgentRequest(BaseModel):
    """Input request for the Strategy Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering entering the healthcare AI market through an "
            "acquisition of a 50-person startup with FDA-cleared algorithms."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
