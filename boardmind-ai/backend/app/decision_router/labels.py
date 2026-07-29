"""Decision Router labels and agent mappings.

Defines business categories and which department agents are relevant
for each category. These mappings are used by the DecisionRouterService
to determine which agents should participate in a deliberation.
"""

# All supported business categories
BUSINESS_CATEGORIES: list[str] = [
    "product_launch",
    "market_expansion",
    "pricing_strategy",
    "hiring",
    "infrastructure_upgrade",
    "digital_transformation",
    "compliance",
    "marketing_campaign",
    "sales_strategy",
    "cost_optimization",
    "business_acquisition",
    "operational_improvement",
    "customer_experience",
    "general_strategic_decision",
]

# Human-readable display names
CATEGORY_DISPLAY_NAMES: dict[str, str] = {
    "product_launch": "Product Launch",
    "market_expansion": "Market Expansion",
    "pricing_strategy": "Pricing Strategy",
    "hiring": "Hiring",
    "infrastructure_upgrade": "Infrastructure Upgrade",
    "digital_transformation": "Digital Transformation",
    "compliance": "Compliance",
    "marketing_campaign": "Marketing Campaign",
    "sales_strategy": "Sales Strategy",
    "cost_optimization": "Cost Optimization",
    "business_acquisition": "Business Acquisition",
    "operational_improvement": "Operational Improvement",
    "customer_experience": "Customer Experience",
    "general_strategic_decision": "General Strategic Decision",
}

# Maps each business category to the relevant department agents.
# Order reflects priority — first agent is considered primary stakeholder.
CATEGORY_AGENT_MAPPING: dict[str, list[str]] = {
    "product_launch": [
        "finance",
        "marketing",
        "sales",
        "it",
        "legal",
        "operations",
        "business_analytics",
    ],
    "market_expansion": [
        "marketing",
        "finance",
        "sales",
        "legal",
        "operations",
        "hr",
        "business_analytics",
    ],
    "pricing_strategy": [
        "finance",
        "sales",
        "marketing",
        "business_analytics",
    ],
    "hiring": [
        "hr",
        "finance",
        "operations",
        "business_analytics",
    ],
    "infrastructure_upgrade": [
        "it",
        "finance",
        "operations",
        "legal",
    ],
    "digital_transformation": [
        "it",
        "operations",
        "finance",
        "hr",
        "business_analytics",
    ],
    "compliance": [
        "legal",
        "it",
        "finance",
        "hr",
        "operations",
    ],
    "marketing_campaign": [
        "marketing",
        "sales",
        "finance",
        "business_analytics",
    ],
    "sales_strategy": [
        "sales",
        "marketing",
        "finance",
        "operations",
        "business_analytics",
    ],
    "cost_optimization": [
        "finance",
        "operations",
        "it",
        "hr",
        "business_analytics",
    ],
    "business_acquisition": [
        "finance",
        "legal",
        "hr",
        "it",
        "operations",
        "marketing",
        "sales",
        "business_analytics",
    ],
    "operational_improvement": [
        "operations",
        "finance",
        "it",
        "business_analytics",
    ],
    "customer_experience": [
        "marketing",
        "sales",
        "operations",
        "it",
        "business_analytics",
    ],
    "general_strategic_decision": [
        "finance",
        "marketing",
        "sales",
        "hr",
        "operations",
        "legal",
        "it",
        "business_analytics",
    ],
}


def get_agents_for_category(category: str) -> list[str]:
    """Return the list of recommended agents for a given business category.

    Falls back to all agents if category is unknown.
    """
    return CATEGORY_AGENT_MAPPING.get(
        category,
        CATEGORY_AGENT_MAPPING["general_strategic_decision"],
    )


def get_display_name(category: str) -> str:
    """Return human-readable name for a category."""
    return CATEGORY_DISPLAY_NAMES.get(category, category.replace("_", " ").title())
