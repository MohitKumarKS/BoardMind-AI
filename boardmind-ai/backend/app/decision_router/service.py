"""Decision Router service.

Receives a business scenario and determines:
1. Business category
2. Relevant department agents
3. Confidence score
4. Routing explanation

This service is completely independent — it does not invoke any agents.
The Orchestrator will call this service to determine participation.
"""

import logging

from .schema import DecisionRouterRequest, DecisionRouterResponse
from .training import predict
from .labels import get_agents_for_category, get_display_name

logger = logging.getLogger(__name__)


class DecisionRouterService:
    """Routes business scenarios to relevant department agents.

    Uses a trained scikit-learn classifier to categorize scenarios
    and maps categories to recommended agent lists.

    Usage:
        service = DecisionRouterService()
        response = service.route(request)
    """

    def route(self, request: DecisionRouterRequest) -> DecisionRouterResponse:
        """Route a business scenario to relevant agents.

        Uses ML classification for the primary category, then expands
        agent selection based on keyword detection for cross-domain scenarios.

        Args:
            request: The business scenario to classify.

        Returns:
            DecisionRouterResponse with category, agents, confidence, and reason.
        """
        category, confidence = predict(request.scenario)
        base_agents = get_agents_for_category(category)

        # Expand agent list based on keyword detection for multi-domain scenarios
        agents = self._expand_agents(request.scenario, base_agents)

        display_name = get_display_name(category)
        reason = self._build_reason(display_name, agents, confidence)

        logger.info(
            f"Routed scenario to '{category}' with confidence {confidence:.2f}, "
            f"recommending {len(agents)} agents"
        )

        return DecisionRouterResponse(
            business_category=category,
            recommended_agents=agents,
            confidence=round(confidence, 3),
            reason=reason,
        )

    def _expand_agents(self, scenario: str, base_agents: list[str]) -> list[str]:
        """Expand agent selection based on keyword detection.

        If the scenario mentions topics relevant to departments not already
        selected, those departments are added. This ensures complex,
        multi-domain scenarios get comprehensive coverage.
        """
        scenario_lower = scenario.lower()
        agents = list(base_agents)

        # Domain keywords that indicate a department should participate
        DOMAIN_SIGNALS: dict[str, list[str]] = {
            "finance": [
                "budget", "roi", "revenue", "cost", "investment", "profit",
                "financial", "capital", "funding", "cash flow", "pricing",
            ],
            "marketing": [
                "marketing", "brand", "campaign", "customer acquisition",
                "market share", "positioning", "go-to-market", "awareness",
                "demand generation", "content strategy",
            ],
            "sales": [
                "sales", "pipeline", "deal", "customer", "revenue growth",
                "account", "quota", "win rate", "churn", "retention",
            ],
            "hr": [
                "hiring", "employee", "talent", "workforce", "reskill",
                "culture", "team", "headcount", "onboarding", "retention",
                "training", "compensation", "people",
            ],
            "operations": [
                "operations", "process", "supply chain", "logistics",
                "delivery", "execution", "capacity", "vendor", "scale",
                "infrastructure", "deployment",
            ],
            "legal": [
                "legal", "compliance", "regulation", "gdpr", "ccpa",
                "contract", "liability", "ip", "patent", "governance",
                "soc2", "iso", "audit", "privacy", "data protection",
            ],
            "it": [
                "technology", "software", "cloud", "migration", "security",
                "cybersecurity", "architecture", "api", "platform",
                "technical", "system", "infrastructure", "ai", "ml",
            ],
            "business_analytics": [
                "analytics", "data", "metrics", "kpi", "forecasting",
                "measurement", "dashboard", "reporting", "insights",
                "benchmark", "performance tracking",
            ],
        }

        # Determine threshold based on scenario complexity
        # Longer scenarios spanning multiple topics need lower threshold
        word_count = len(scenario_lower.split())
        match_threshold = 1 if word_count > 40 else 2

        for agent_id, keywords in DOMAIN_SIGNALS.items():
            if agent_id in agents:
                continue
            matches = sum(1 for kw in keywords if kw in scenario_lower)
            if matches >= match_threshold:
                agents.append(agent_id)

        return agents

    def _build_reason(
        self, display_name: str, agents: list[str], confidence: float
    ) -> str:
        """Build a human-readable routing explanation."""
        agent_names = ", ".join(
            a.replace("_", " ").title() for a in agents[:4]
        )
        remaining = len(agents) - 4

        explanation = (
            f"This scenario is classified as '{display_name}' "
            f"(confidence: {confidence:.0%}). "
            f"Recommended department perspectives: {agent_names}"
        )

        if remaining > 0:
            explanation += f", and {remaining} more"

        explanation += "."

        if confidence < 0.4:
            explanation += (
                " Note: Classification confidence is low — consider including "
                "all departments for a comprehensive analysis."
            )

        return explanation
