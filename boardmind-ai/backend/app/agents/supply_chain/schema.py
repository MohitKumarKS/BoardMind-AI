"""Supply Chain Agent response schema.

Pydantic models matching the Output Schema defined in the Supply Chain Agent specification.
These models define the contract for structured output from the Chief Supply Chain Officer Agent.
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


class OperationalRisk(str, Enum):
    """Operational risk classification for supply chain."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SupplyChainDomainAssessment(BaseModel):
    """Structured supply chain impact analysis.

    Every field must contain a substantive supply chain assessment with
    clear reasoning tied to logistics, procurement, and vendor management.
    """

    supply_chain_impact: str = Field(
        ...,
        description="Effect on supply chain operations and throughput",
        examples=["Requires new fulfillment center in APAC region; adds 3-5 day lead time reduction for 40% of orders"],
    )
    vendor_dependency: str = Field(
        ...,
        description="Supplier risk and concentration analysis",
        examples=["Single-source dependency on 2 critical components; 6-month lead time if primary supplier fails"],
    )
    logistics_complexity: str = Field(
        ...,
        description="Distribution and fulfillment challenges assessment",
        examples=["Cross-border logistics add 15% cost overhead; requires customs brokerage partnerships in 3 new markets"],
    )
    procurement_needs: str = Field(
        ...,
        description="Sourcing requirements and procurement strategy",
        examples=["Need to qualify 3 new suppliers within 90 days; estimated procurement cost increase of 8-12% at current volumes"],
    )
    operational_risk: OperationalRisk = Field(
        ...,
        description="Overall supply chain operational risk classification",
    )


class SupplyChainAgentResponse(BaseModel):
    """Complete structured response from the Supply Chain Agent.

    This schema enforces the output contract defined in the Supply Chain Agent
    specification. All fields are required to ensure comprehensive analysis.
    """

    agent_id: str = Field(
        default="supply_chain",
        description="Unique identifier for the Supply Chain department agent",
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
    domain_assessment: SupplyChainDomainAssessment = Field(
        ...,
        description="Structured supply chain impact analysis",
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
        description="Detailed supply chain reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific, actionable supply chain risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for supply chain support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended supply chain KPIs to monitor",
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


class SupplyChainAgentRequest(BaseModel):
    """Input request for the Supply Chain Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering reshoring our manufacturing from China to Mexico "
            "to reduce lead times and mitigate geopolitical supply chain risk."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
