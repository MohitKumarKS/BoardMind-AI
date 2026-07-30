"""AI Governance & Ethics Officer response schema.

Pydantic models matching the Output Schema for the AI Governance Agent.
These models enforce structured output for AI ethics, algorithmic fairness,
and responsible AI deployment analysis.
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


class AIRiskLevel(str, Enum):
    """AI risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AIGovernanceDomainAssessment(BaseModel):
    """Structured AI governance and ethics impact analysis.

    Every field must contain a substantive assessment covering ethical risks,
    transparency, governance frameworks, and societal implications.
    """

    ethical_risk: str = Field(
        ...,
        description="Bias, fairness, and discrimination concerns in AI systems",
        examples=["High bias risk in hiring algorithm: training data underrepresents 3 protected groups; disparate impact likely without mitigation"],
    )
    transparency_requirements: str = Field(
        ...,
        description="Explainability and interpretability needs for AI decisions",
        examples=["LIME/SHAP explanations required for all credit decisions per regulatory expectations; model cards needed for deployment"],
    )
    governance_framework: str = Field(
        ...,
        description="AI governance policies, oversight mechanisms, and accountability structures",
        examples=["Requires AI Ethics Board review, model risk management tier classification, and ongoing monitoring per NIST AI RMF"],
    )
    societal_impact: str = Field(
        ...,
        description="Broader societal implications of AI deployment",
        examples=["Automated decision-making affects 50K+ individuals annually; requires human-in-the-loop for adverse decisions"],
    )
    ai_risk_level: AIRiskLevel = Field(
        ...,
        description="Overall AI risk classification",
    )

    @field_validator("ethical_risk")
    @classmethod
    def ethical_risk_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Ethical risk assessment must be detailed and specific.")
        return v

    @field_validator("transparency_requirements")
    @classmethod
    def transparency_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Transparency requirements must be detailed and specific.")
        return v

    @field_validator("governance_framework")
    @classmethod
    def governance_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Governance framework assessment must be detailed and specific.")
        return v

    @field_validator("societal_impact")
    @classmethod
    def societal_must_be_specific(cls, v: str) -> str:
        if len(v) < 20:
            raise ValueError("Societal impact assessment must be detailed and specific.")
        return v


class AIGovernanceAgentResponse(BaseModel):
    """Complete structured response from the AI Governance & Ethics Officer.

    This schema enforces the output contract for comprehensive AI governance
    analysis covering ethics, fairness, transparency, and societal impact.
    """

    agent_id: str = Field(
        default="ai_governance",
        description="Unique identifier for the AI Governance department agent",
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
    domain_assessment: AIGovernanceDomainAssessment = Field(
        ...,
        description="Structured AI governance and ethics impact analysis",
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
        description="Detailed AI governance reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific AI ethics and governance risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Requirements that must be met for responsible AI deployment",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended AI governance KPIs to monitor",
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


class AIGovernanceAgentRequest(BaseModel):
    """Input request for the AI Governance Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze from an AI governance perspective",
        examples=[
            "We are planning to deploy an AI-powered hiring screening tool that will "
            "automatically filter resumes and rank candidates for 500+ open positions annually."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
