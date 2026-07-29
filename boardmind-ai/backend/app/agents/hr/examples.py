"""HR Agent example scenarios."""

from .schema import HRAgentRequest

SCENARIO_MASS_HIRING = HRAgentRequest(
    scenario=(
        "Engineering requests 8 additional software engineers to accelerate development. "
        "Current team is 12. This would represent 67% headcount growth in one department "
        "within a 3-month hiring window."
    ),
    context="Average time-to-hire for engineers in our market: 45 days. Current team culture is tight-knit and collaborative.",
)

SCENARIO_REMOTE_TO_OFFICE = HRAgentRequest(
    scenario=(
        "Leadership wants to mandate 4 days/week in-office starting next quarter. "
        "Currently the policy is 2 days/week. 40% of the team was hired as remote-first "
        "during 2021-2022."
    ),
    context="Employee engagement score: 72. Last policy change (3→2 days) increased eNPS by 15 points. 3 competitors offer full remote.",
)

SCENARIO_RESTRUCTURE = HRAgentRequest(
    scenario=(
        "We are merging the Product and Engineering departments into a single 'Product & Technology' "
        "organization. This eliminates the VP Product role and creates a new CTO/CPO hybrid position."
    ),
    context="VP Product has been with company 5 years. Both teams have distinct cultures. Total affected: 45 people.",
)

SCENARIO_PERFORMANCE_SYSTEM = HRAgentRequest(
    scenario=(
        "Finance proposes implementing a stack-ranking performance system to identify "
        "bottom 10% performers for performance improvement plans. Goal is to 'raise the bar' "
        "on talent quality."
    ),
    context="Current system is goal-based with manager discretion. Employee satisfaction with current reviews: 68%.",
)

SCENARIO_OFFSHORE_TEAM = HRAgentRequest(
    scenario=(
        "Operations proposes establishing a 20-person offshore development team in India "
        "to reduce engineering costs by 40%. Onshore team would focus on architecture "
        "and complex features while offshore handles implementation."
    ),
    context="Current team: 30 engineers, all onshore. No prior offshore experience. Team morale is high.",
)

ALL_SCENARIOS = [
    ("Mass Hiring", SCENARIO_MASS_HIRING),
    ("Remote to Office Mandate", SCENARIO_REMOTE_TO_OFFICE),
    ("Department Restructure", SCENARIO_RESTRUCTURE),
    ("Stack Ranking System", SCENARIO_PERFORMANCE_SYSTEM),
    ("Offshore Team Setup", SCENARIO_OFFSHORE_TEAM),
]

ALL_EXAMPLE_RESPONSES = []
