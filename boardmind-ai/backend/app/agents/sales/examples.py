"""Sales Agent example scenarios and expected responses."""

from .schema import (
    SalesAgentRequest,
    SalesAgentResponse,
    SalesDomainAssessment,
    Position,
    PipelineImpact,
    DealCycleEffect,
    CompetitiveEffect,
)

SCENARIO_NEW_PRODUCT = SalesAgentRequest(
    scenario=(
        "We're launching an AI analytics product at $2,000/month targeting mid-market. "
        "Sales team believes 50 customers achievable in Year 1. Need to build "
        "new sales playbook and potentially hire 2 account executives."
    ),
    context="Current sales team: 6 AEs focused on enterprise ($50K+ ACV). Mid-market is new territory.",
)

SCENARIO_PRICE_INCREASE = SalesAgentRequest(
    scenario=(
        "Finance proposes 25% price increase for new customers, grandfathering "
        "existing accounts for 12 months. Current ACV is $36K."
    ),
    context="Win rate is 32%. Top competitor is priced 20% higher. 15 deals in pipeline worth $2.1M.",
)

SCENARIO_PARTNERSHIP = SalesAgentRequest(
    scenario=(
        "A Fortune 500 company wants to white-label our product for their customer base "
        "of 2,000 mid-market companies. They propose a 40% revenue share arrangement."
    ),
    context="Our current direct sales reach: 200 accounts/year. Partner's distribution: immediate access to 2,000.",
)

SCENARIO_FEATURE_DELAY = SalesAgentRequest(
    scenario=(
        "Engineering says the enterprise SSO and audit logging features will be "
        "delayed 3 months. These features are in 8 active enterprise deals worth $1.2M total."
    ),
    context="3 of those deals close in 60 days. Competitors all offer SSO. Workaround exists but is manual.",
)

SCENARIO_VERTICAL_EXPANSION = SalesAgentRequest(
    scenario=(
        "Marketing wants us to expand into healthcare vertical. Requires HIPAA "
        "compliance features and industry-specific positioning. Estimated 6-month "
        "development timeline."
    ),
    context="Healthcare TAM for our category: $1.8B. We have 3 healthcare prospects in pipeline already asking for compliance.",
)

EXAMPLE_RESPONSE_PRICE_INCREASE = SalesAgentResponse(
    agent_id="sales",
    round=1,
    position=Position.SUPPORT,
    confidence=0.75,
    domain_assessment=SalesDomainAssessment(
        revenue_upside=(
            "At current pipeline volume, 25% price increase yields $525K additional ACV "
            "from the 15 deals in pipeline ($2.1M × 25%). Full-year impact: $1.2-1.8M "
            "additional ARR assuming pipeline replenishment at similar volume."
        ),
        revenue_risk=(
            "Win rate may drop 3-5 points (32% → 27-29%) as price-sensitive prospects "
            "choose alternatives. Estimated revenue at risk: $300-400K from lost deals "
            "that would have closed at current pricing."
        ),
        pipeline_impact=PipelineImpact.ACCELERATION,
        deal_cycle_effect=DealCycleEffect.LONGER,
        competitive_effect=CompetitiveEffect.ADVANTAGE,
    ),
    summary=(
        "Support the price increase — we're leaving money on the table at current pricing, "
        "and the competitor price gap gives us room to move up without losing position."
    ),
    rationale=(
        "Our current pricing at $36K ACV is 20% below the top competitor. Buyers who choose "
        "us are not primarily price-driven — our win rate drivers are product quality and "
        "support experience. A 25% increase to $45K ACV still positions us below the "
        "competitor, maintaining our 'premium value at fair price' narrative.\n\n"
        "The 15 deals currently in pipeline were qualified at $36K. For deals past "
        "negotiation stage, I recommend honoring the original pricing to protect "
        "relationships. Net-new pipeline should enter at the new price point. This creates "
        "a clean transition without disrupting deals in flight.\n\n"
        "I expect a temporary dip in win rate (2-4 points) as the sales team adjusts "
        "messaging to justify the higher price. This requires updated value frameworks "
        "and objection handling training. Within one quarter, I expect win rates to "
        "stabilize as the team builds confidence at the new price.\n\n"
        "The grandfathering approach for existing customers is essential — it protects "
        "NRR and prevents churn conversations that distract from new business."
    ),
    risks=[
        "Win rate may drop 3-5 points during transition quarter as team adjusts to new pricing conversations",
        "3-5 price-sensitive prospects in current pipeline may stall or choose competitor",
        "Sales cycle may extend 1-2 weeks as buyers require additional justification at higher price point",
        "Competitor may respond with aggressive discounting to capture our price-sensitive segment",
    ],
    conditions=[
        "Honor existing pipeline pricing for deals past qualification stage",
        "Provide sales team with updated value selling framework and objection handling within 2 weeks",
        "Allow deal-level discounting authority (up to 10%) for strategic accounts during first quarter",
        "Monitor win rate weekly — if drop exceeds 5 points for 4 consecutive weeks, trigger pricing review",
    ],
    customer_impact=(
        "Existing customers are protected by 12-month grandfathering — no immediate "
        "churn risk. New prospects will face higher price but remain below market rate. "
        "Strategic accounts in pipeline should be honored at original pricing to preserve "
        "trust. Net impact on customer relationships: neutral to slightly positive as "
        "higher price signals premium positioning."
    ),
    references_to=[],
)

ALL_SCENARIOS = [
    ("New Product Sales", SCENARIO_NEW_PRODUCT),
    ("Price Increase", SCENARIO_PRICE_INCREASE),
    ("White-Label Partnership", SCENARIO_PARTNERSHIP),
    ("Feature Delay Impact", SCENARIO_FEATURE_DELAY),
    ("Vertical Expansion", SCENARIO_VERTICAL_EXPANSION),
]

ALL_EXAMPLE_RESPONSES = [
    ("Price Increase", EXAMPLE_RESPONSE_PRICE_INCREASE),
]
