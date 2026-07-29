"""Finance Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Finance Agent's output quality
2. Demonstrating the expected style of financial reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    FinanceAgentRequest,
    FinanceAgentResponse,
    FinanceDomainAssessment,
    Position,
    RiskLevel,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_NEW_PRODUCT_LAUNCH = FinanceAgentRequest(
    scenario=(
        "We are considering launching a new B2B SaaS product targeting mid-market "
        "companies (500-2000 employees). The product is an AI-powered analytics dashboard. "
        "Estimated development cost is $400K over 6 months, with a target price of "
        "$2,000/month per customer. Our sales team believes we can acquire 50 customers "
        "in Year 1 and 150 by Year 2."
    ),
    context="Current runway is 18 months. Monthly burn rate is $180K. We have $3.2M in the bank.",
)

SCENARIO_MARKET_EXPANSION = FinanceAgentRequest(
    scenario=(
        "Our US-based e-commerce platform is considering expanding into the European market "
        "(starting with UK and Germany). This would require local warehousing, multilingual "
        "customer support, GDPR compliance infrastructure, and localized marketing. "
        "The European market represents approximately 30% of our total addressable market."
    ),
    context=(
        "Current US revenue is $12M ARR growing 40% YoY. We have not operated internationally before. "
        "A competitor entered Europe last year and captured 8% market share in 6 months."
    ),
)

SCENARIO_ENGINEERING_HIRING = FinanceAgentRequest(
    scenario=(
        "The engineering team is requesting approval to hire 8 additional software engineers "
        "to accelerate product development. Current team size is 12 engineers. The VP of "
        "Engineering claims this will reduce the product roadmap timeline from 18 months to "
        "10 months, enabling earlier market entry for three planned features."
    ),
    context=(
        "Average fully-loaded engineer cost in our market is $185K/year. Current engineering "
        "budget is $2.2M/year. The three features are projected to generate $3.5M in "
        "additional ARR within 12 months of launch."
    ),
)

SCENARIO_AI_INFRASTRUCTURE = FinanceAgentRequest(
    scenario=(
        "The CTO proposes investing in dedicated AI/ML infrastructure: GPU cluster, "
        "MLOps platform, and a 3-person ML engineering team. This would replace our "
        "current approach of using third-party AI APIs (OpenAI, Anthropic) which costs "
        "$45K/month and is growing 25% month-over-month as usage scales."
    ),
    context=(
        "Current AI API spend: $45K/month ($540K/year). Proposed infrastructure: $1.2M "
        "upfront + $30K/month operational. ML team: $600K/year fully loaded. "
        "Our AI features drive 60% of new customer acquisition."
    ),
)

SCENARIO_NEW_OFFICE = FinanceAgentRequest(
    scenario=(
        "Leadership is proposing opening a second office in Austin, TX to support "
        "growth and access a broader talent pool. The plan includes a 15,000 sq ft "
        "office lease, relocation packages for 5 senior leaders, and hiring 30 local "
        "employees over 18 months."
    ),
    context=(
        "Current headcount: 85 (all in San Francisco). SF office lease expires in 14 months. "
        "Austin average salary is 20% below SF for equivalent roles. "
        "Remote work policy allows 2 days WFH but leadership wants in-person collaboration."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_NEW_PRODUCT = FinanceAgentResponse(
    agent_id="finance",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.65,
    domain_assessment=FinanceDomainAssessment(
        revenue_impact=(
            "Projected $1.2M ARR by end of Year 1 (50 customers × $24K/year), "
            "scaling to $3.6M ARR by Year 2 (150 customers). "
            "Assumes 0% churn in Year 1, which is optimistic for a new product."
        ),
        cost_impact=(
            "Development: $400K (one-time). Ongoing: estimated $80K/month for "
            "infrastructure, support, and maintenance ($960K/year). "
            "Customer acquisition cost estimated at $8K-$12K per customer based on "
            "B2B SaaS benchmarks for mid-market."
        ),
        roi_estimate=(
            "Projected 85-120% ROI by end of Year 2, assuming sales projections hold. "
            "Break-even requires minimum 35 customers at current cost structure. "
            "Assumptions: 90% gross margin on SaaS, $10K blended CAC, <5% monthly churn."
        ),
        payback_period=(
            "14-20 months from launch, depending on sales ramp speed. "
            "Best case (50 customers by month 8): 14 months. "
            "Conservative case (50 customers by month 14): 20 months."
        ),
        risk_level=RiskLevel.MEDIUM,
    ),
    summary=(
        "Conditionally support with phased investment — financials work if "
        "sales projections are validated with pre-launch commitments."
    ),
    rationale=(
        "The unit economics are attractive at $2,000/month with expected SaaS margins of "
        "85-90%. At 50 customers, the product generates $1.2M ARR against an estimated "
        "$960K annual operating cost, yielding positive contribution margin in Year 1. "
        "However, the sales projection of 50 customers in Year 1 is unvalidated.\n\n"
        "The $400K development investment represents 12.5% of our current cash reserves "
        "($3.2M) and approximately 2.2 months of burn. While this is within acceptable "
        "limits, it reduces our runway from 18 months to approximately 15.5 months, "
        "assuming no revenue offset during the development period.\n\n"
        "The primary financial concern is the gap between development completion and "
        "revenue realization. We will have spent $400K before generating any product "
        "revenue, and the sales cycle for mid-market B2B is typically 3-6 months. "
        "This creates a 9-12 month cash exposure period.\n\n"
        "I recommend a phased approach: invest $150K in an MVP with 3-5 design partners "
        "who commit to paid pilots before authorizing the remaining $250K."
    ),
    risks=[
        "Sales projection of 50 customers in Year 1 is unvalidated — B2B SaaS benchmarks suggest 30-40 is more realistic for a new entrant",
        "Cash runway reduction from 18 to 15.5 months increases funding pressure if product underperforms",
        "Customer acquisition cost may exceed $12K in mid-market segment given lack of existing brand awareness",
        "Monthly burn increase of $80K for ongoing operations reduces time to next funding decision",
    ],
    conditions=[
        "Secure at least 5 paid pilot commitments ($1K+/month) before full development authorization",
        "Cap total investment at $500K (development + first 3 months operations) as a stage gate",
        "Achieve 20 paying customers within 6 months of launch or trigger formal review",
        "Maintain minimum 12 months runway at all times during the initiative",
    ],
    metrics_to_track=[
        "Monthly Recurring Revenue (MRR) and growth rate",
        "Customer Acquisition Cost (CAC) — target below $10K",
        "Net Revenue Retention (NRR) — target above 100%",
        "Burn rate impact — monthly cash consumption vs. plan",
        "Months to break-even on fully-loaded cost basis",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_AI_INFRASTRUCTURE = FinanceAgentResponse(
    agent_id="finance",
    round=1,
    position=Position.SUPPORT,
    confidence=0.75,
    domain_assessment=FinanceDomainAssessment(
        revenue_impact=(
            "Indirect: AI features drive 60% of new customer acquisition. "
            "Protecting this capability protects ~$7.2M of the current $12M ARR trajectory. "
            "No direct new revenue, but cost avoidance of $200K+/year at current growth rates."
        ),
        cost_impact=(
            "Year 1 total: $1.2M infrastructure + $600K team + $360K operations = $2.16M. "
            "Current trajectory (API costs growing 25% MoM): projected $1.08M Year 1, "
            "$2.7M Year 2 at current growth. Crossover point is Month 16."
        ),
        roi_estimate=(
            "3-year NPV positive at ~$1.4M assuming current API cost growth continues. "
            "ROI of 65% over 3 years. Assumptions: 25% MoM API growth slows to 15% "
            "after 6 months, in-house costs remain stable after initial buildout."
        ),
        payback_period=(
            "16-20 months from initial investment, based on avoided API costs exceeding "
            "infrastructure + team costs. Faster if AI usage growth continues above 20% MoM."
        ),
        risk_level=RiskLevel.MEDIUM,
    ),
    summary=(
        "Support the infrastructure investment — the current API cost trajectory "
        "is unsustainable and the crossover math works within 16-20 months."
    ),
    rationale=(
        "The financial case rests on a straightforward cost trajectory analysis. Current "
        "AI API spend of $540K/year is growing at 25% month-over-month. If this growth "
        "continues even at a reduced 15% MoM rate, API costs will exceed $2.7M in Year 2. "
        "The proposed in-house solution costs $2.16M in Year 1 and approximately $960K/year "
        "ongoing thereafter.\n\n"
        "The crossover point — where cumulative in-house costs become cheaper than cumulative "
        "API costs — occurs at approximately Month 16. Beyond that point, every month "
        "generates positive cost avoidance. The 3-year NPV at a 10% discount rate is "
        "approximately $1.4M positive.\n\n"
        "Additionally, there is a strategic risk consideration: AI features drive 60% of "
        "new customer acquisition. Dependency on third-party APIs for a core competitive "
        "advantage creates vendor concentration risk. While I do not quantify strategic "
        "value (that is not my domain), the financial exposure of a 30% API price increase "
        "would be $160K+ annually at current volumes.\n\n"
        "The primary financial risk is execution: if the ML team takes longer than planned "
        "to build equivalent capabilities, we pay both API costs AND infrastructure costs "
        "during the transition period."
    ),
    risks=[
        "Dual-cost period during transition: paying both API fees and infrastructure costs simultaneously could total $150K/month for 4-6 months",
        "ML team hiring timeline may extend beyond plan — each month of delay costs approximately $45K in continued API spend above plan",
        "Infrastructure costs may exceed estimate if GPU demand spikes — recommend 20% cost buffer ($240K)",
        "If AI feature growth slows below 15% MoM, payback extends beyond 24 months and NPV turns marginal",
    ],
    conditions=[
        "Negotiate API cost cap or volume discount as bridge during 6-month transition period",
        "Phase infrastructure spend: $400K initial, $800K released only after successful pilot workloads",
        "Establish clear performance benchmarks — in-house must match API quality within 4 months of deployment",
        "Include $240K contingency buffer (20%) in the approved budget",
    ],
    metrics_to_track=[
        "Monthly AI infrastructure cost vs. projected API cost (avoidance tracking)",
        "ML model performance parity vs. third-party API benchmarks",
        "Time to full transition — target 6 months from team start",
        "Cost per inference: in-house vs. API (unit economics)",
        "AI feature conversion rate — must not degrade during transition",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("New Product Launch", SCENARIO_NEW_PRODUCT_LAUNCH),
    ("European Market Expansion", SCENARIO_MARKET_EXPANSION),
    ("Engineering Team Expansion", SCENARIO_ENGINEERING_HIRING),
    ("AI Infrastructure Investment", SCENARIO_AI_INFRASTRUCTURE),
    ("New Office Opening", SCENARIO_NEW_OFFICE),
]

ALL_EXAMPLE_RESPONSES = [
    ("New Product Launch", EXAMPLE_RESPONSE_NEW_PRODUCT),
    ("AI Infrastructure Investment", EXAMPLE_RESPONSE_AI_INFRASTRUCTURE),
]
