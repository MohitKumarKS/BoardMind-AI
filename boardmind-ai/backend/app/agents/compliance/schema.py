"""Compliance Officer Agent response schema.

Pydantic models for the Chief Compliance Officer agent.
Focuses on regulatory compliance, policy adherence, audit readiness,
and governance frameworks.
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


class ComplianceStatus(str, Enum):
    """Regulatory compliance classification."""

    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REQUIRES_REVIEW = "requires_review"


class ComplianceDomainAssessment(BaseModel):
    """Structured compliance assessment from the CCO perspective.

    Every field must contain a substantive compliance analysis — generic
    responses violate the Compliance Agent's design constraints.
    """

    regulatory_impact: str = Field(
        ...,
        description="Regulations affected by the proposal",
        examples=["Directly impacts GDPR (Articles 6, 13, 35), SOX Section 404 internal controls, and PCI-DSS Requirement 3 (stored cardholder data). May trigger CCPA notification requirements for California residents."],
    )
    compliance_gaps: str = Field(
        ...,
        description="Identified compliance gaps that must be addressed",
        examples=["Three material gaps identified: (1) No Data Protection Impact Assessment for new processing, (2) Third-party processor agreements lack required Article 28 clauses, (3) Retention policy undefined for new data category."],
    )
    remediation_effort: str = Field(
        ...,
        description="Effort required to achieve full compliance",
        examples=["Estimated 8-12 weeks remediation: DPIA completion (2 weeks), contract amendments (4 weeks legal review), policy updates and training (2 weeks), audit documentation (2-4 weeks)."],
    )
    audit_readiness: str = Field(
        ...,
        description="Impact on audit posture and readiness",
        examples=["Current SOC2 Type II audit cycle unaffected if remediation completes before Q3 audit window. Annual SOX assessment will require updated control documentation. Recommend pre-audit readiness review."],
    )
    compliance_status: ComplianceStatus = Field(
        default=ComplianceStatus.REQUIRES_REVIEW,
        description="Overall compliance classification",
    )


class ComplianceAgentResponse(BaseModel):
    """Complete structured response from the Compliance Agent.

    This schema enforces the output contract for the CCO agent.
    All fields are required to ensure comprehensive compliance analysis.
    """

    agent_id: str = Field(
        default="compliance",
        description="Unique identifier for the Compliance agent",
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
    domain_assessment: ComplianceDomainAssessment = Field(
        ...,
        description="Structured compliance assessment",
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
        description="Detailed compliance reasoning (2-4 paragraphs)",
    )
    risks: list[str] = Field(
        ...,
        min_length=1,
        description="Specific compliance risks identified",
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Compliance requirements that must be met for support",
    )
    metrics_to_track: list[str] = Field(
        ...,
        min_length=1,
        description="Recommended compliance KPIs to monitor",
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


class ComplianceAgentRequest(BaseModel):
    """Input request for the Compliance Agent in Department Workspace mode."""

    scenario: str = Field(
        ...,
        min_length=20,
        description="The business proposal or scenario to analyze",
        examples=[
            "We are considering collecting additional user behavior data "
            "for our recommendation engine, including browsing patterns "
            "and purchase history across our European customer base."
        ],
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context or constraints (optional)",
    )
