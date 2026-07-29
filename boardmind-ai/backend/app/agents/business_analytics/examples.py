"""Business Analytics Agent example scenarios."""

from .schema import AnalyticsAgentRequest

SCENARIO_CONVERSION_OPTIMIZATION = AnalyticsAgentRequest(
    scenario=(
        "Product team claims that redesigning the onboarding flow will increase "
        "trial-to-paid conversion by 25%. They base this on qualitative user feedback "
        "and one competitor's published case study."
    ),
    context="Current conversion rate: 12%. Industry average: 15-18%. Last onboarding change (6 months ago) had no measurable impact.",
)

SCENARIO_MARKET_SIZE = AnalyticsAgentRequest(
    scenario=(
        "Marketing estimates our Total Addressable Market at $5B based on a third-party "
        "analyst report. They propose a $2M investment to capture 1% market share "
        "within 18 months."
    ),
    context="Current revenue: $8M. Growth rate: 30% YoY. The analyst report is 2 years old and covers a broader category.",
)

SCENARIO_CHURN_PREDICTION = AnalyticsAgentRequest(
    scenario=(
        "Customer Success wants to build a churn prediction model using historical "
        "data to proactively intervene with at-risk accounts. They project 30% "
        "churn reduction within 6 months."
    ),
    context="Current annual churn: 18%. 3 years of customer data available. No existing predictive models. CS team: 8 people.",
)

SCENARIO_PRICING_EXPERIMENT = AnalyticsAgentRequest(
    scenario=(
        "Revenue team proposes A/B testing three new pricing tiers to optimize ARPU. "
        "Test would run for 6 weeks on 20% of new signups. Expected uplift: 15-25% ARPU."
    ),
    context="Current ARPU: $420/month. 800 new signups/month. No prior pricing experiments. Single pricing tier currently.",
)

SCENARIO_EMPLOYEE_PRODUCTIVITY = AnalyticsAgentRequest(
    scenario=(
        "Management claims that the new AI copilot tool increased developer productivity "
        "by 40%. They want to expand it company-wide based on a 2-week pilot with "
        "8 volunteer developers."
    ),
    context="Total engineering team: 45. Pilot was opt-in (volunteers). No control group. Productivity measured by self-reported time savings.",
)

ALL_SCENARIOS = [
    ("Conversion Optimization", SCENARIO_CONVERSION_OPTIMIZATION),
    ("Market Size Validation", SCENARIO_MARKET_SIZE),
    ("Churn Prediction Model", SCENARIO_CHURN_PREDICTION),
    ("Pricing Experiment", SCENARIO_PRICING_EXPERIMENT),
    ("Productivity Claims", SCENARIO_EMPLOYEE_PRODUCTIVITY),
]

ALL_EXAMPLE_RESPONSES = []
