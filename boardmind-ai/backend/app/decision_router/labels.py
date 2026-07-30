"""Decision Router labels and agent mappings.

Defines business categories and which department agents are relevant
for each category. These mappings are used by the DecisionRouterService
to determine which agents should participate in a deliberation.

Updated to include all 20 executive agents across all categories.
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
    "cybersecurity",
    "sustainability",
    "innovation",
    "investor_communications",
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
    "cybersecurity": "Cybersecurity",
    "sustainability": "Sustainability & ESG",
    "innovation": "Innovation & Research",
    "investor_communications": "Investor Communications",
    "general_strategic_decision": "General Strategic Decision",
}

# Maps each business category to the relevant department agents.
# Order reflects priority — first agent is considered primary stakeholder.
# Updated to include all 20 agents where appropriate.
CATEGORY_AGENT_MAPPING: dict[str, list[str]] = {
    "product_launch": [
        "ceo",
        "finance",
        "marketing",
        "sales",
        "product",
        "it",
        "legal",
        "operations",
        "customer_success",
        "business_analytics",
        "innovation",
        "investor_relations",
    ],
    "market_expansion": [
        "ceo",
        "strategy",
        "marketing",
        "finance",
        "sales",
        "legal",
        "compliance",
        "operations",
        "supply_chain",
        "hr",
        "risk",
        "business_analytics",
        "investor_relations",
    ],
    "pricing_strategy": [
        "finance",
        "sales",
        "marketing",
        "product",
        "customer_success",
        "business_analytics",
        "strategy",
        "investor_relations",
    ],
    "hiring": [
        "hr",
        "finance",
        "operations",
        "ceo",
        "business_analytics",
    ],
    "infrastructure_upgrade": [
        "it",
        "ciso",
        "finance",
        "operations",
        "legal",
        "risk",
        "innovation",
    ],
    "digital_transformation": [
        "ceo",
        "it",
        "operations",
        "finance",
        "hr",
        "ai_governance",
        "innovation",
        "ciso",
        "business_analytics",
        "strategy",
    ],
    "compliance": [
        "compliance",
        "legal",
        "ciso",
        "it",
        "finance",
        "hr",
        "operations",
        "risk",
        "esg",
        "ai_governance",
    ],
    "marketing_campaign": [
        "marketing",
        "sales",
        "finance",
        "product",
        "customer_success",
        "business_analytics",
    ],
    "sales_strategy": [
        "sales",
        "marketing",
        "finance",
        "operations",
        "customer_success",
        "product",
        "business_analytics",
        "strategy",
    ],
    "cost_optimization": [
        "finance",
        "operations",
        "it",
        "hr",
        "supply_chain",
        "business_analytics",
        "ceo",
    ],
    "business_acquisition": [
        "ceo",
        "finance",
        "legal",
        "strategy",
        "hr",
        "it",
        "operations",
        "risk",
        "compliance",
        "marketing",
        "sales",
        "investor_relations",
        "business_analytics",
    ],
    "operational_improvement": [
        "operations",
        "finance",
        "it",
        "supply_chain",
        "hr",
        "business_analytics",
    ],
    "customer_experience": [
        "customer_success",
        "marketing",
        "sales",
        "product",
        "operations",
        "it",
        "business_analytics",
    ],
    "cybersecurity": [
        "ciso",
        "it",
        "compliance",
        "risk",
        "legal",
        "ceo",
        "finance",
        "ai_governance",
    ],
    "sustainability": [
        "esg",
        "ceo",
        "operations",
        "supply_chain",
        "compliance",
        "finance",
        "investor_relations",
        "legal",
        "strategy",
    ],
    "innovation": [
        "innovation",
        "it",
        "product",
        "strategy",
        "finance",
        "ai_governance",
        "ceo",
        "business_analytics",
    ],
    "investor_communications": [
        "investor_relations",
        "ceo",
        "finance",
        "strategy",
        "legal",
        "compliance",
    ],
    "general_strategic_decision": [
        "ceo",
        "finance",
        "strategy",
        "marketing",
        "sales",
        "hr",
        "operations",
        "legal",
        "it",
        "business_analytics",
        "risk",
        "compliance",
        "ciso",
        "product",
        "customer_success",
        "supply_chain",
        "esg",
        "ai_governance",
        "innovation",
        "investor_relations",
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
