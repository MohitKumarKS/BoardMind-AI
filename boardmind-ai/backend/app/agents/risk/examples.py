"""Chief Risk Officer Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Risk Agent's output quality
2. Demonstrating the expected style of risk reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    RiskAgentRequest,
    RiskAgentResponse,
    RiskDomainAssessment,
    Position,
    RiskLevel,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_NEW_MARKET_ENTRY = RiskAgentRequest(
    scenario=(
        "We are considering entering the healthcare vertical with our "
        "analytics platform. This requires HIPAA compliance, BAA agreements "
        "with all vendors, and specialized data handling. Healthcare represents "
        "a $50B TAM but we have zero experience in regulated industries."
    ),
    context=(
        "Current verticals: SaaS, e-commerce, fintech (non-regulated). "
        "No HIPAA infrastructure in place. Competitor entered healthcare 2 years "
        "ago and captured $8M ARR. HIPAA violations carry penalties up to "
        "$1.5M per incident category per year."
    ),
)

SCENARIO_VENDOR_CONCENTRATION = RiskAgentRequest(
    scenario=(
        "Our entire production infrastructure runs on a single cloud provider "
        "(AWS). The CTO proposes deepening this dependency by adopting 5 additional "
        "AWS-native services (Aurora, SQS, Step Functions, Bedrock, Kendra) to "
        "accelerate development speed. This would increase switching costs significantly."
    ),
    context=(
        "Current AWS spend: $180K/month. Estimated post-adoption: $280K/month. "
        "AWS outage last year caused 4 hours downtime ($200K revenue impact). "
        "Multi-cloud alternative would cost 30% more but reduce concentration risk. "
        "AWS provides 20% volume discount at current commitment."
    ),
)

SCENARIO_AGGRESSIVE_GROWTH = RiskAgentRequest(
    scenario=(
        "The board is pushing for 3x growth in 18 months, requiring us to "
        "simultaneously expand into 3 new markets, hire 100 people, and launch "
        "2 new products. Current growth rate is 40% YoY. The plan requires "
        "$15M in additional capital and operational capacity we don't yet have."
    ),
    context=(
        "Current ARR: $12M. Team size: 85. Burn rate: $1.2M/month. "
        "Runway: 14 months at current burn. Historical success rate of "
        "companies attempting 3x growth in 18 months: approximately 20%. "
        "Our current infrastructure supports 2x capacity before requiring "
        "major re-architecture."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_HEALTHCARE = RiskAgentResponse(
    agent_id="risk",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.70,
    domain_assessment=RiskDomainAssessment(
        risk_exposure=(
            "Maximum exposure: $4.5M (HIPAA penalties up to $1.5M/category/year × "
            "3 likely violation categories during learning curve) plus $1.5M in "
            "remediation costs and $1.5M in reputation damage. Expected loss: "
            "$1.8M based on 40% probability of compliance incident in Year 1."
        ),
        probability_assessment=(
            "40% probability of at least one HIPAA compliance incident in first "
            "12 months based on: zero regulated industry experience, new compliance "
            "infrastructure (immature), and industry data showing 60% of new entrants "
            "experience compliance issues. Reduces to 15% with proper preparation."
        ),
        mitigation_strategy=(
            "Recommended: (1) 6-month compliance readiness phase before taking "
            "healthcare customers — reduces incident probability from 40% to 15%. "
            "(2) Hire experienced HIPAA compliance officer ($200K). (3) Engage "
            "specialized compliance consultant for first year ($150K). (4) Cyber "
            "liability insurance with regulatory coverage ($100K/year premium). "
            "Total mitigation investment: $450K. Reduces expected loss from $1.8M to $500K."
        ),
        residual_risk=(
            "Post-mitigation residual risk: $500K expected loss (within risk appetite "
            "for strategic growth initiatives). Residual probability: 15%. Acceptable "
            "given potential $8M ARR upside. Risk-reward ratio: 1:16 (favorable)."
        ),
        risk_level=RiskLevel.HIGH,
    ),
    summary=(
        "Conditionally support healthcare entry — risk exposure is manageable "
        "with a 6-month compliance readiness phase, but entering without "
        "preparation exceeds our risk appetite by 3x."
    ),
    rationale=(
        "The healthcare vertical presents a classic high-risk/high-reward scenario. "
        "The $50B TAM and proven competitor traction ($8M ARR) validate the opportunity. "
        "However, our zero experience in regulated industries creates substantial "
        "compliance risk. HIPAA violations are not theoretical — they carry penalties "
        "up to $1.5M per incident category per year.\n\n"
        "My probability assessment is based on industry data: organizations entering "
        "regulated verticals without prior experience have a 40-60% compliance incident "
        "rate in their first year. This is not a technology problem — it's a process "
        "and culture gap. Our current team has never operated under regulatory "
        "constraints, and compliance muscle memory takes time to develop.\n\n"
        "The risk becomes acceptable with proper preparation. A 6-month readiness "
        "phase (compliance infrastructure, training, hiring, insurance) reduces "
        "incident probability from 40% to 15% and maximum exposure from $4.5M to "
        "$1.5M. The investment of $450K in risk mitigation is highly efficient "
        "given it protects against $4.5M in potential losses."
    ),
    risks=[
        "HIPAA compliance incident in Year 1 — 40% probability without preparation, carrying up to $1.5M/category in penalties",
        "Reputation contagion — healthcare compliance failure could damage trust in non-healthcare customer base",
        "Resource diversion — compliance infrastructure absorbs engineering capacity, slowing core product development by estimated 20%",
        "Regulatory escalation — initial violation triggers enhanced scrutiny, increasing probability and severity of subsequent findings",
    ],
    conditions=[
        "Complete 6-month compliance readiness program before accepting first healthcare customer",
        "Hire dedicated HIPAA compliance officer with minimum 5 years healthcare compliance experience",
        "Achieve independent HIPAA readiness assessment score above 85% before market entry",
        "Secure cyber liability insurance with specific regulatory penalty coverage of minimum $3M",
    ],
    metrics_to_track=[
        "HIPAA readiness score — independent assessment, quarterly, target >90%",
        "Compliance incident count — target zero in first 12 months of operation",
        "Risk appetite utilization — healthcare initiative vs. total risk budget allocation",
        "Time to compliance maturity — benchmark against industry average of 18 months",
        "Loss event probability — Bayesian update monthly based on near-misses and audit findings",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Healthcare Market Entry", SCENARIO_NEW_MARKET_ENTRY),
    ("Vendor Concentration Risk", SCENARIO_VENDOR_CONCENTRATION),
    ("Aggressive Growth Plan", SCENARIO_AGGRESSIVE_GROWTH),
]

ALL_EXAMPLE_RESPONSES = [
    ("Healthcare Market Entry", EXAMPLE_RESPONSE_HEALTHCARE),
]
