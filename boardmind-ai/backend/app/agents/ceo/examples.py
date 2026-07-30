"""CEO Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the CEO Agent's output quality
2. Demonstrating the expected style of strategic reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    CEOAgentRequest,
    CEOAgentResponse,
    CEODomainAssessment,
    Position,
    RiskLevel,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_STRATEGIC_PIVOT = CEOAgentRequest(
    scenario=(
        "We are considering a strategic pivot from B2C to B2B enterprise. "
        "Our B2C product has 50K users but low monetization ($5 ARPU). "
        "Enterprise prospects are willing to pay $50K-$200K annually for "
        "a customized version of our core technology. This would require "
        "rebuilding our sales motion, hiring enterprise AEs, and potentially "
        "reducing B2C investment."
    ),
    context=(
        "Current ARR: $3M (B2C). Three enterprise pilots closed at $75K each. "
        "B2C growth has stalled at 5% QoQ. Enterprise pipeline shows $2M potential. "
        "Board is pushing for path to profitability within 18 months."
    ),
)

SCENARIO_ACQUISITION = CEOAgentRequest(
    scenario=(
        "A competitor with complementary technology and 200 enterprise customers "
        "is available for acquisition at $45M (3.5x revenue). They have strong "
        "technology but are burning $2M/month with 8 months runway. Their customer "
        "base overlaps 15% with ours. Integration would take 12-18 months."
    ),
    context=(
        "Our current valuation: $180M. Cash reserves: $60M. Last funding round "
        "was Series C at $150M. The target's technology would save us 2 years of "
        "R&D. Two other potential acquirers are circling."
    ),
)

SCENARIO_MARKET_EXPANSION = CEOAgentRequest(
    scenario=(
        "Our VP of International proposes expanding into Asia-Pacific, starting "
        "with Japan and Australia. This requires local teams, localized product, "
        "and regional partnerships. APAC represents 35% of our TAM but requires "
        "significant cultural adaptation of our product and go-to-market."
    ),
    context=(
        "US market share: 12%. No international presence. Two competitors already "
        "have APAC operations. Customer demand signals from 40+ APAC prospects. "
        "Japan requires local data residency compliance."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_PIVOT = CEOAgentResponse(
    agent_id="ceo",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.72,
    domain_assessment=CEODomainAssessment(
        strategic_alignment=(
            "Strongly aligned with board mandate for path to profitability. "
            "Enterprise economics ($50K-$200K ACV) fundamentally change our "
            "unit economics and align with the 18-month profitability target. "
            "However, this represents a significant identity shift from our "
            "original B2C mission."
        ),
        stakeholder_impact=(
            "Shareholders: Positive — enterprise path offers clearer profitability. "
            "Employees: Mixed — B2C team (40% of staff) faces role changes or reductions. "
            "Current B2C customers: Negative — reduced investment in their product. "
            "Board: Strongly positive — addresses their core concern directly."
        ),
        competitive_positioning=(
            "Moves us into a less crowded segment where our technology differentiation "
            "matters more. B2B competitors lack our AI capabilities. Early enterprise "
            "traction ($225K from 3 pilots) validates product-market fit. Risk: "
            "B2B incumbents have deeper enterprise sales expertise."
        ),
        execution_priority=(
            "P0 — this is an existential strategic decision. Recommend immediate "
            "dedicated task force with CEO direct oversight. Decision deadline: "
            "end of current quarter. Delay costs $150K/month in continued "
            "low-ROI B2C spend."
        ),
        risk_level=RiskLevel.HIGH,
    ),
    summary=(
        "Conditionally support the B2B pivot — the enterprise economics are "
        "compelling but execution requires a deliberate transition plan that "
        "preserves optionality on the B2C base."
    ),
    rationale=(
        "The strategic case for an enterprise pivot is strong: $5 ARPU vs. "
        "$50K-$200K ACV is a 10,000x improvement in unit economics. Three closed "
        "enterprise pilots at $75K validate that the market will pay. With B2C "
        "growth stalling at 5% QoQ and a board mandate for profitability in 18 "
        "months, the B2C path alone cannot achieve that target.\n\n"
        "However, this is not a simple feature add — it's a fundamental strategic "
        "transformation. Our culture, hiring, sales motion, product development "
        "cadence, and customer success model all change. The 40% of employees "
        "focused on B2C will face significant disruption. I will not approve a "
        "'flip the switch' approach — we need a 6-month transition plan.\n\n"
        "My recommendation: maintain B2C at current investment levels (no increase) "
        "while aggressively building the enterprise muscle. If enterprise ARR "
        "reaches $1M within 6 months, commit fully to the pivot. If not, reassess. "
        "This preserves optionality while testing the enterprise hypothesis at scale."
    ),
    risks=[
        "Identity crisis — trying to serve both B2C and B2B simultaneously may result in mediocrity at both",
        "Talent gap — enterprise sales and customer success require fundamentally different skills than our current team possesses",
        "Customer backlash — B2C users discovering reduced investment may generate negative PR and brand damage",
        "Execution timeline — enterprise sales cycles are 3-6 months, meaning revenue validation takes 9+ months",
    ],
    conditions=[
        "Develop a 6-month transition plan with clear milestones before committing resources",
        "Achieve $1M enterprise ARR within 6 months as the commitment threshold",
        "Retain core B2C team for 6 months to avoid burning bridges prematurely",
        "Board alignment on transition timeline and acceptable B2C revenue decline during shift",
    ],
    metrics_to_track=[
        "Enterprise ARR and pipeline growth — monthly tracking against $1M threshold",
        "Enterprise win rate and average sales cycle length",
        "B2C retention rate during transition — target no more than 10% incremental churn",
        "Employee retention in critical roles — flag departures above 15%",
        "Time-to-close for enterprise deals vs. industry benchmark (90 days)",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_ACQUISITION = CEOAgentResponse(
    agent_id="ceo",
    round=1,
    position=Position.SUPPORT,
    confidence=0.70,
    domain_assessment=CEODomainAssessment(
        strategic_alignment=(
            "Highly aligned — acquisition accelerates our technology roadmap by "
            "2 years and adds 200 enterprise customers. This directly supports "
            "our stated goal of enterprise market leadership. The 3.5x revenue "
            "multiple is reasonable given distressed timing."
        ),
        stakeholder_impact=(
            "Shareholders: Positive — accretive within 12 months if integration succeeds. "
            "Employees: Significant uncertainty during 12-18 month integration. "
            "Customers: Positive — combined product offering is stronger. "
            "Board: Will require careful positioning given $45M cash deployment."
        ),
        competitive_positioning=(
            "Eliminates a competitor while gaining complementary technology and "
            "200 customers. Creates combined entity that is clearly #1 or #2 in "
            "category. Prevents two other acquirers from gaining these assets."
        ),
        execution_priority=(
            "P0 — time-sensitive due to competing acquirers and target's 8-month "
            "runway. Decision needed within 30 days. Recommend immediate due "
            "diligence team activation."
        ),
        risk_level=RiskLevel.HIGH,
    ),
    summary=(
        "Support the acquisition — the strategic value of eliminating a competitor, "
        "gaining 200 customers, and saving 2 years of R&D justifies the $45M at "
        "this distressed timing."
    ),
    rationale=(
        "This is a rare strategic opportunity: a complementary competitor at a "
        "reasonable multiple during a moment of vulnerability. The $45M price "
        "represents 3.5x their revenue, which is below market norms of 5-8x for "
        "healthy SaaS companies. Their distressed position (8 months runway, $2M "
        "monthly burn) gives us negotiating leverage and urgency.\n\n"
        "Strategically, this acquisition solves three problems simultaneously: "
        "it eliminates a competitor, adds 200 enterprise logos (with only 15% "
        "overlap), and saves us an estimated 2 years of R&D investment. The "
        "combined entity would have a significantly stronger competitive position.\n\n"
        "The primary risk is integration execution. 12-18 months is a long period "
        "of organizational disruption. We must maintain momentum on our core "
        "business while absorbing their team and technology. I recommend a "
        "dedicated integration PMO with a senior leader as integration czar."
    ),
    risks=[
        "Integration complexity — 12-18 month timeline creates prolonged organizational uncertainty and potential talent flight",
        "Cash deployment — $45M reduces our reserves from $60M to $15M, significantly limiting future flexibility",
        "Cultural mismatch — their team is in survival mode which creates different work norms and expectations",
        "Competing acquirers may drive up price if bidding war develops",
    ],
    conditions=[
        "Complete technical due diligence confirming technology integration feasibility within 30 days",
        "Negotiate price to $38-42M given their distressed position and our leverage",
        "Secure retention packages for top 20 technical talent at the target company",
        "Board approval with clear integration budget and timeline authority",
    ],
    metrics_to_track=[
        "Integration milestone completion vs. 18-month plan",
        "Combined customer retention — target 90%+ retention across both bases",
        "Key talent retention at acquired company — target 80%+ of identified critical roles",
        "Revenue synergy realization — track cross-sell and upsell within combined customer base",
        "Time-to-product-integration — target full platform merge within 12 months",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Strategic B2B Pivot", SCENARIO_STRATEGIC_PIVOT),
    ("Competitor Acquisition", SCENARIO_ACQUISITION),
    ("APAC Market Expansion", SCENARIO_MARKET_EXPANSION),
]

ALL_EXAMPLE_RESPONSES = [
    ("Strategic B2B Pivot", EXAMPLE_RESPONSE_PIVOT),
    ("Competitor Acquisition", EXAMPLE_RESPONSE_ACQUISITION),
]
