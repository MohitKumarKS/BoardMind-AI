"""Decision Router module.

Classifies business scenarios and recommends relevant department agents.
Uses scikit-learn TF-IDF + LinearSVC pipeline trained on built-in data.

Usage:
    from app.decision_router import DecisionRouterService, DecisionRouterRequest

    service = DecisionRouterService()
    request = DecisionRouterRequest(scenario="Your business scenario here")
    response = service.route(request)
"""

from .schema import DecisionRouterRequest, DecisionRouterResponse
from .service import DecisionRouterService
from .labels import BUSINESS_CATEGORIES, CATEGORY_AGENT_MAPPING

__all__ = [
    "DecisionRouterService",
    "DecisionRouterRequest",
    "DecisionRouterResponse",
    "BUSINESS_CATEGORIES",
    "CATEGORY_AGENT_MAPPING",
]
