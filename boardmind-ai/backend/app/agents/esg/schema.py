"""ESG & Sustainability Officer response schema.

Pydantic models matching the Output Schema defined in the ESG Agent specification.
These models enforce structured output for environmental, social, and governance analysis.
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


class ESGRiskLevel(str, Enum):
    """ESG risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ESGDomainAssessment(BaseModel):
    """Structured ESG impact analysis.

    Every field must contain a substantive assessment covering environmental,
    social, and governance dimensions with reference to established frameworks.
    """

    environmental_impact: str = Field(
        ...,
        description="Carbon footprint, resource usage, emissions, and environmental consequences",
        examples=["Estimated 2,400 tonnes CO2e annual increase from expanded data center operations; requires offset strategy"],
    )
    social_impact: str = Field(
        ...,
        description="Community impact, diversity implications, labor practices",
        examples=["Positive workforce diversity impact: 35% increase in underrepresented groups in technical roles"],
    )
    governance_implications: str = Field(
        ...,
        description="Board oversight requirements, transparency needs, ethical considerations",
        examples=["Requires new board-level ESG committee oversight and quarterly sustainability reporting"],
    )
    sustainability_score: str = Field(
        ...,
        description="Alignment with ESG frameworks (GRI, SASB, TCFD)",
        examples=["Aligns with GRI 305 (Emissions) and TCFD climate risk disclosure; gaps in SASB materiality mapping"],
    )
    esg_risk: ESGRiskLevel = Field(
        ...,
        description="Overall ESG risk classification",
    )

    @field_validator("environmental_impact")
    @classmethod
    def environmental_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Environmental impact assessment must be detailed and specific.")
        return v

    @field_validator("social_impact")
    @classmethod
    def social_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Social impact assessment must be detailed and specific.")
        return v

    @field_validator("governance_implications")
    @classmethod
    def governance_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Governance implications must be detailed and specific.")
        return v

    @field_validator("sustainability_score")
    @classmethod
    def sustainability_must_reference_framework(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Sustainability score must reference specific ESG frameworks.")
        return v


class ESGAgentResponse(BaseModel):
    """Complete structured response from the ESG & Sustainability Officer.

    This schema enforces the output contract for comprehensive ESG analysis
    covering environmental, social, and governance dimensions.
    """

    agent_id: str = Field(
        default="esg",
        description="Unique identifier for the ESG department agent",
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
    domain_assessment: ESGDomainAssessment = Field(
        ...,
        description="Structured ESG impact analysis",
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
        description="Detailed ESG reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific ESG risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for ESG approval",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended ESG KPIs to monitor",
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


class ESGAgentRequest(BaseModel):
    """Input request for the ESG Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze from an ESG perspective",
        examples=[
            "We are considering expanding our manufacturing operations to a new facility "
            "that would increase production capacity by 40% but require significant energy usage."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
