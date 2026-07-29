"""Decision Router request and response schemas."""

from pydantic import BaseModel, Field


class DecisionRouterRequest(BaseModel):
    """Input request for the Decision Router."""

    scenario: str = Field(
        ...,
        min_length=10,
        description="The business scenario to classify and route",
        examples=["We are considering launching a new SaaS product targeting enterprise customers"],
    )


class DecisionRouterResponse(BaseModel):
    """Output response from the Decision Router."""

    business_category: str = Field(
        ...,
        description="The classified business category",
        examples=["product_launch"],
    )
    recommended_agents: list[str] = Field(
        ...,
        min_length=1,
        description="Ordered list of recommended department agents",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score in the classification (0.0-1.0)",
    )
    reason: str = Field(
        ...,
        description="Human-readable explanation of the routing decision",
    )
