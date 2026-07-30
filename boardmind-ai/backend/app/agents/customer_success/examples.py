"""Customer Success Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Customer Success Agent's output quality
2. Demonstrating the expected style of customer-centric reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    CustomerSuccessAgentRequest,
    CustomerSuccessAgentResponse,
    CustomerSuccessDomainAssessment,
    Position,
    CustomerRisk,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_PLATFORM_MIGRATION = CustomerSuccessAgentRequest(
    scenario=(
        "We are planning a mandatory migration of all customers from our legacy v2 "
        "platform to the new v3 architecture. The migration window is 6 months with "
        "a hard cutover date. V3 has 90% feature parity but 10% of v2 features are "
        "being deprecated. Affected features are used by approximately 25% of customers."
    ),
    context=(
        "Current customer base: 450 accounts. NPS: 38. Health score distribution: "
        "60% green, 25% yellow, 15% red. Average contract value: $48K ARR. "
        "Top 10 accounts represent 35% of revenue. 3 red-zone accounts have "
        "renewal dates within the migration window."
    ),
)

SCENARIO_PRICING_CHANGE = CustomerSuccessAgentRequest(
    scenario=(
        "Finance is proposing a 20% price increase across all plans effective next "
        "quarter. Existing customers would see the increase at their next renewal date. "
        "The increase is needed to fund infrastructure investments and maintain margins. "
        "No additional features or value is being added alongside the price increase."
    ),
    context=(
        "Current NPS: 42. Customer tenure distribution: 30% < 1 year, 45% 1-3 years, "
        "25% > 3 years. Competitor pricing: we are currently 10% below market average. "
        "Last price increase was 18 months ago (10%). Churn rate: 8% annual."
    ),
)

SCENARIO_FEATURE_LAUNCH = CustomerSuccessAgentRequest(
    scenario=(
        "Product is launching a major new analytics module that changes the core "
        "dashboard experience. The new module is opt-in for 60 days, then becomes "
        "the default. Current dashboard is the #1 most-used feature (92% weekly "
        "engagement). The new module adds significant capability but changes navigation."
    ),
    context=(
        "Beta feedback from 50 customers: 70% positive, 20% neutral, 10% negative. "
        "Negative feedback primarily from power users with custom dashboard layouts. "
        "CSAT for current dashboard: 4.3/5. Power users represent 15% of users but "
        "35% of revenue."
    ),
)

SCENARIO_SUPPORT_REDUCTION = CustomerSuccessAgentRequest(
    scenario=(
        "Operations is proposing to reduce phone support hours from 24/7 to business "
        "hours only (8am-6pm local time) and replace off-hours coverage with AI chatbot. "
        "Goal is to reduce support costs by 40%. Current off-hours ticket volume is "
        "15% of total but includes 30% of critical severity tickets."
    ),
    context=(
        "Current support CSAT: 4.4/5. Average response time: 8 minutes (phone), "
        "2 hours (email). Critical ticket SLA: 15 minutes to first response. "
        "Enterprise tier customers (40% of revenue) have 24/7 support in their contracts. "
        "AI chatbot pilot resolved 45% of off-hours tickets satisfactorily."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_MIGRATION = CustomerSuccessAgentResponse(
    agent_id="customer_success",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.6,
    domain_assessment=CustomerSuccessDomainAssessment(
        customer_impact=(
            "All 450 accounts affected. 25% (112 accounts) lose actively-used features. "
            "Top-10 accounts (35% of revenue) require white-glove migration support. "
            "15% of accounts (68) are already in red health zone — forced migration adds "
            "additional stress to relationships already at risk."
        ),
        retention_risk=(
            "High churn risk: estimated 5-8% incremental churn concentrated in accounts "
            "affected by deprecated features and those in red/yellow health zones. "
            "3 red-zone accounts with renewals during migration window represent $420K ARR "
            "at immediate risk. Worst case: 12% churn if migration is poorly communicated."
        ),
        satisfaction_forecast=(
            "NPS projected to drop from 38 to 28-32 during migration peak (months 2-4). "
            "Recovery to pre-migration levels expected by month 9 if new platform delivers "
            "promised improvements. Risk: if NPS drops below 30, negative word-of-mouth "
            "compounds and recovery takes 12+ months."
        ),
        support_requirements=(
            "60% increase in support ticket volume for 3-month peak period. Need: "
            "4 dedicated migration support specialists, updated knowledge base (50+ articles), "
            "video migration guides, and weekly office hours webinars. CSM capacity: "
            "each CSM needs 30% bandwidth allocation for migration-related outreach."
        ),
        customer_risk=CustomerRisk.HIGH,
    ),
    summary=(
        "Conditionally support migration with significantly extended timeline and "
        "mandatory customer communication plan — current 6-month window is too aggressive "
        "for our health score distribution."
    ),
    rationale=(
        "The migration is strategically sound for long-term customer health — v3 offers "
        "genuine improvements that will enhance customer outcomes. However, the proposed "
        "6-month mandatory timeline is concerning given our current health score distribution. "
        "With 15% of accounts already in red zone and 25% in yellow, forcing a major platform "
        "change adds stress to relationships that are already fragile.\n\n"
        "The 25% of customers losing actively-used features represents our highest churn risk. "
        "These accounts need alternatives or workarounds identified before migration begins. "
        "Without this, we're effectively telling a quarter of our customer base that their "
        "workflows are no longer supported — a classic churn trigger.\n\n"
        "I recommend extending the timeline to 9-12 months with three waves: willing early "
        "adopters (green accounts) first, followed by mainstream (yellow), then careful "
        "migration of red-zone accounts with executive-sponsored transition plans. The 3 "
        "red-zone accounts renewing during migration need immediate CSM engagement to "
        "secure renewals before any migration communication begins."
    ),
    risks=[
        "3 red-zone accounts ($420K ARR) renewing during migration window may not renew if migration disrupts their critical workflows",
        "25% of customers losing features will experience immediate negative impact — without alternatives, this is a direct churn trigger",
        "NPS below 30 creates negative word-of-mouth that affects acquisition and expansion, compounding revenue impact beyond direct churn",
        "Support team overwhelm during peak migration period degrades experience for ALL customers, not just migrating ones",
    ],
    conditions=[
        "Extend migration window to 9-12 months with phased rollout (green → yellow → red accounts)",
        "Identify alternatives or workarounds for all deprecated features before announcing migration to affected customers",
        "Secure renewal commitments from 3 at-risk accounts before any migration communication begins",
        "Deploy dedicated migration support team (4 specialists) with 48-hour response SLA for migration issues",
    ],
    metrics_to_track=[
        "NPS by migration wave — alert if any wave drops more than 8 points below baseline",
        "Churn rate for migration cohort vs. control — target no more than 3% incremental",
        "Health score transitions: track accounts moving from green → yellow or yellow → red during migration",
        "Support ticket volume and CSAT during migration — maintain CSAT above 4.0/5",
        "Feature deprecation impact: track adoption of alternative workflows by affected customers",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_PRICING = CustomerSuccessAgentResponse(
    agent_id="customer_success",
    round=1,
    position=Position.OPPOSE,
    confidence=0.72,
    domain_assessment=CustomerSuccessDomainAssessment(
        customer_impact=(
            "All 450 accounts affected at renewal. Highest impact on price-sensitive "
            "segments: customers < 1 year (30% of base) have lowest switching costs. "
            "Long-tenured customers (> 3 years, 25% of base) will feel entitled to "
            "grandfathered rates. No value-add to justify increase creates entitlement gap."
        ),
        retention_risk=(
            "Projected 3-5% incremental churn above baseline 8%. Concentrated in: "
            "< 1 year tenure (highest switching cost tolerance), red/yellow health accounts "
            "(looking for reasons to leave). A 20% increase with no added value gives "
            "dissatisfied customers a concrete trigger to begin vendor evaluation."
        ),
        satisfaction_forecast=(
            "NPS projected to decline 5-8 points from 42 to 34-37 within 90 days of "
            "first renewal cohort experiencing increase. CSAT for renewal process will "
            "drop significantly. Recovery unlikely without value demonstration — price "
            "increases without value create lasting perception of unfairness."
        ),
        support_requirements=(
            "Estimated 200+ price-related support contacts in first 30 days. CSMs need "
            "talking points and authority to offer limited concessions for strategic accounts. "
            "Executive escalation path required for top-tier accounts. Renewal conversations "
            "become adversarial rather than partnership-focused."
        ),
        customer_risk=CustomerRisk.HIGH,
    ),
    summary=(
        "Oppose the 20% price increase without corresponding value delivery — customers "
        "will perceive this as extraction rather than fair exchange, triggering evaluation cycles."
    ),
    rationale=(
        "From a customer success perspective, a 20% price increase with no additional value "
        "is the worst possible scenario for retention. Our NPS of 42 is healthy but not "
        "exceptional — we don't have the customer loyalty reserves to absorb a purely "
        "extractive price action. When customers feel they're paying more for the same "
        "thing, it triggers vendor evaluation cycles that we may not win.\n\n"
        "The timing makes this worse: our last increase was only 18 months ago. Customers "
        "will perceive a pattern of escalating costs. The fact that we're still 10% below "
        "market average is irrelevant from a customer psychology perspective — they compare "
        "to what they paid before, not to what competitors charge.\n\n"
        "If a price increase is financially necessary, I strongly recommend coupling it with "
        "a tangible value delivery (new features, improved SLAs, expanded usage limits) and "
        "reducing the increase to 10-12% maximum. Additionally, loyal customers (> 3 years) "
        "should receive preferential treatment. The revenue uplift from a gentler increase "
        "paired with lower churn will outperform an aggressive increase with higher attrition."
    ),
    risks=[
        "20% increase triggers vendor evaluation in 15-20% of accounts — each evaluation creates 50% churn probability",
        "Long-tenured customers (25% of base) feel betrayed by lack of loyalty recognition, creating vocal detractors",
        "Renewal conversations become adversarial — CSMs lose consultative positioning and become defensive",
        "NPS decline below 35 creates negative review and word-of-mouth cycle affecting new customer acquisition",
    ],
    conditions=[
        "Reduce increase to maximum 12% and bundle with tangible value (expanded limits, new features, better SLA)",
        "Provide loyalty discount: customers with 3+ year tenure receive maximum 8% increase",
        "Allow CSMs discretionary authority to offer 6-month price lock for strategic/at-risk accounts",
        "Communicate increase with 90-day advance notice and clear articulation of value delivered since last increase",
    ],
    metrics_to_track=[
        "Renewal rate by cohort: track accounts renewing at new price vs. churning — alert if below 90%",
        "NPS at 30/60/90 days post-renewal for affected accounts — compare to pre-increase baseline",
        "Expansion revenue: track whether price increase erodes upsell pipeline (customers less willing to expand)",
        "Competitive mention rate in exit surveys — track if pricing becomes top-3 churn reason",
        "CSM-flagged at-risk accounts: track volume increase post-announcement as early warning signal",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Platform Migration", SCENARIO_PLATFORM_MIGRATION),
    ("Pricing Increase", SCENARIO_PRICING_CHANGE),
    ("Feature Launch", SCENARIO_FEATURE_LAUNCH),
    ("Support Hours Reduction", SCENARIO_SUPPORT_REDUCTION),
]

ALL_EXAMPLE_RESPONSES = [
    ("Platform Migration", EXAMPLE_RESPONSE_MIGRATION),
    ("Pricing Increase", EXAMPLE_RESPONSE_PRICING),
]
