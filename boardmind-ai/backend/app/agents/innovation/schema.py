"""Chief Innovation Officer response schema.

Pydantic models matching the Output Schema for the Innovation Agent.
These models enforce structured output for R&D strategy, emerging technology
assessment, innovation pipeline, and intellectual property analysis.
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


class InnovationRiskLevel(str, Enum):
    """Innovation risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InnovationDomainAssessment(BaseModel):
    """Structured innovation and R&D impact analysis.

    Every field must contain a substantive assessment covering novelty,
    technology readiness, research requirements, and IP opportunity.
    """

    innovation_potential: str = Field(
        ...,
        description="Novelty and breakthrough potential of the proposal",
        examples=["High innovation potential: combines two emerging technologies (federated learning + edge AI) with no direct market precedent"],
    )
    technology_readiness: str = Field(
        ...,
        description="Technology Readiness Level (TRL) and maturity assessment",
        examples=["TRL 4-5: validated in laboratory environment; requires 12-18 months of engineering to reach TRL 7 (system prototype in operational environment)"],
    )
    research_requirements: str = Field(
        ...,
        description="R&D investment, timeline, and resource needs",
        examples=["Requires $2M R&D investment over 18 months: 4 senior researchers, access to GPU cluster, partnership with university lab"],
    )
    ip_opportunity: str = Field(
        ...,
        description="Intellectual property and patent potential",
        examples=["3-5 patentable innovations identified in novel architecture; freedom-to-operate analysis shows clear white space"],
    )
    innovation_risk: InnovationRiskLevel = Field(
        ...,
        description="Overall innovation risk classification",
    )

    @field_validator("innovation_potential")
    @classmethod
    def innovation_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Innovation potential assessment must be detailed and specific.")
        return v

    @field_validator("technology_readiness")
    @classmethod
    def trl_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Technology readiness assessment must be detailed and specific.")
        return v

    @field_validator("research_requirements")
    @classmethod
    def research_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Research requirements must be detailed and specific.")
        return v

    @field_validator("ip_opportunity")
    @classmethod
    def ip_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("IP opportunity assessment must be detailed and specific.")
        return v


class InnovationAgentResponse(BaseModel):
    """Complete structured response from the Chief Innovation Officer.

    This schema enforces the output contract for comprehensive innovation
    analysis covering R&D strategy, technology readiness, and IP opportunity.
    """

    agent_id: str = Field(
        default="innovation",
        description="Unique identifier for the Innovation department agent",
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
    domain_assessment: InnovationDomainAssessment = Field(
        ...,
        description="Structured innovation and R&D impact analysis",
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
        description="Detailed innovation reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific innovation and R&D risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for innovation success",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended innovation KPIs to monitor",
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


class InnovationAgentRequest(BaseModel):
    """Input request for the Innovation Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze from an innovation perspective",
        examples=[
            "We are considering investing in quantum computing research to develop "
            "a competitive advantage in cryptographic services within 3-5 years."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
