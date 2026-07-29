"""HR Agent response schema.

Pydantic models matching the Output Schema defined in the HR Agent specification.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"


class HeadcountChange(str, Enum):
    HIRING = "hiring"
    REDUCTION = "reduction"
    REDEPLOYMENT = "redeployment"
    NONE = "none"


class SkillGap(str, Enum):
    NONE = "none"
    MINOR = "minor"
    SIGNIFICANT = "significant"


class CultureImpact(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class ChangeComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class HRDomainAssessment(BaseModel):
    """Structured people impact analysis."""

    headcount_change: HeadcountChange = Field(
        ..., description="Type of workforce change required"
    )
    skill_gap: SkillGap = Field(
        ..., description="Severity of skill gaps to address"
    )
    culture_impact: CultureImpact = Field(
        ..., description="Effect on organizational culture"
    )
    change_complexity: ChangeComplexity = Field(
        ..., description="Complexity of organizational change management"
    )
    timeline_to_readiness: str = Field(
        ..., description="Estimated time for people readiness"
    )


class HRAgentResponse(BaseModel):
    """Complete structured response from the HR Agent."""

    agent_id: str = Field(default="hr")
    round: int = Field(default=1, ge=1, le=3)
    position: Position = Field(...)
    confidence: float = Field(..., ge=0.0, le=1.0)
    domain_assessment: HRDomainAssessment = Field(...)
    summary: str = Field(..., min_length=10, max_length=300)
    rationale: str = Field(..., min_length=100)
    risks: list[str] = Field(..., min_length=1)
    conditions: list[str] = Field(default_factory=list)
    change_management_needs: list[str] = Field(
        ..., min_length=1, description="Actions needed to prepare people for the change"
    )
    references_to: list[str] = Field(default_factory=list)

    @field_validator("risks")
    @classmethod
    def risks_must_be_specific(cls, v: list[str]) -> list[str]:
        for risk in v:
            if len(risk) < 10:
                raise ValueError(f"Risk '{risk}' is too vague.")
        return v


class HRAgentRequest(BaseModel):
    """Input request for the HR Agent."""

    scenario: str = Field(..., min_length=20)
    context: Optional[str] = Field(default=None)
