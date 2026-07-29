"""Decision Router API route.

Provides endpoint for classifying business scenarios and
determining which department agents should participate.
"""

from fastapi import APIRouter

from app.decision_router import (
    DecisionRouterService,
    DecisionRouterRequest,
    DecisionRouterResponse,
)

router = APIRouter()

service = DecisionRouterService()


@router.post("/", response_model=DecisionRouterResponse)
def route_scenario(request: DecisionRouterRequest) -> DecisionRouterResponse:
    """Classify a business scenario and recommend relevant department agents.

    Accepts a business scenario and returns:
    - The classified business category
    - Ordered list of recommended department agents
    - Confidence score in the classification
    - Human-readable routing explanation
    """
    return service.route(request)
