"""Legal Agent example scenarios."""

from .schema import LegalAgentRequest

SCENARIO_DATA_PRODUCT = LegalAgentRequest(
    scenario=(
        "We want to launch a product that collects user behavioral data to provide "
        "personalized recommendations. Data would be stored in US-based servers but "
        "we plan to serve customers in EU and California."
    ),
    context="No existing privacy framework. No DPO appointed. Current Terms of Service are 3 years old.",
)

SCENARIO_ACQUISITION = LegalAgentRequest(
    scenario=(
        "We are considering acquiring a 15-person startup for their AI technology. "
        "They have 2 patents pending and several open-source dependencies in their "
        "core product. Purchase price: $4M."
    ),
    context="Startup has 3 existing customer contracts with enterprise clients. No disclosed litigation.",
)

SCENARIO_PARTNERSHIP = LegalAgentRequest(
    scenario=(
        "A competitor proposes a joint venture to co-develop a new product category. "
        "They would contribute distribution, we contribute technology. Revenue split: 60/40."
    ),
    context="Both companies serve overlapping customer segments. Antitrust considerations may apply.",
)

SCENARIO_EMPLOYEE_DATA = LegalAgentRequest(
    scenario=(
        "HR wants to implement AI-based performance monitoring that tracks employee "
        "productivity metrics including screen time, communication frequency, and "
        "project completion velocity."
    ),
    context="Remote workforce across 5 US states and 2 EU countries. No existing employee monitoring policy.",
)

SCENARIO_OPEN_SOURCE = LegalAgentRequest(
    scenario=(
        "Engineering proposes open-sourcing our core analytics library under MIT license "
        "to build community and attract developer talent. The library contains algorithms "
        "that are key differentiators in our product."
    ),
    context="Library was built by employees on company time. 2 former contractors contributed code. No CLA exists.",
)

ALL_SCENARIOS = [
    ("Data Product Launch", SCENARIO_DATA_PRODUCT),
    ("Startup Acquisition", SCENARIO_ACQUISITION),
    ("Competitor Partnership", SCENARIO_PARTNERSHIP),
    ("Employee Monitoring", SCENARIO_EMPLOYEE_DATA),
    ("Open Source Strategy", SCENARIO_OPEN_SOURCE),
]

ALL_EXAMPLE_RESPONSES = []
