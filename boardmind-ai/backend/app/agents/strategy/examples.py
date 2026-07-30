"""Strategy Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Strategy Agent's output quality
2. Demonstrating the expected style of strategic reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    StrategyAgentRequest,
    StrategyAgentResponse,
    StrategyDomainAssessment,
    Position,
    StrategicPriority,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_MARKET_ENTRY = StrategyAgentRequest(
    scenario=(
        "We are considering entering the healthcare AI market through acquisition "
        "of a 50-person startup with FDA-cleared algorithms. The target has $3M ARR, "
        "growing 80% YoY, and owns 12 patents in medical imaging AI. Asking price "
        "is $45M (15x ARR)."
    ),
    context=(
        "Our current market is enterprise data analytics ($8B TAM). Healthcare AI "
        "TAM is $12B growing at 25% CAGR. We have no healthcare domain expertise "
        "but strong AI/ML capabilities. Two competitors entered healthcare last year."
    ),
)

SCENARIO_GEOGRAPHIC_EXPANSION = StrategyAgentRequest(
    scenario=(
        "Our North American SaaS platform is evaluating expansion into Asia-Pacific, "
        "specifically Japan and Australia. The APAC market for our category is growing "
        "at 30% CAGR vs 15% in NA. We would need local data centers, partnerships "
        "with regional system integrators, and localized go-to-market."
    ),
    context=(
        "Current NA market share: 12%. APAC competitors: 3 strong local players with "
        "60% combined share. Our largest enterprise customer has APAC operations and "
        "has requested regional support. Two PE-backed competitors are also eyeing APAC."
    ),
)

SCENARIO_PLATFORM_PIVOT = StrategyAgentRequest(
    scenario=(
        "The board is considering pivoting from a point-solution SaaS to a platform "
        "model with third-party developer ecosystem. This would require opening APIs, "
        "building a marketplace, developer relations team, and fundamentally changing "
        "our go-to-market from direct sales to product-led growth."
    ),
    context=(
        "Current ARR: $25M, 200 enterprise customers. Platform competitors (Salesforce, "
        "HubSpot) are 50-100x our size. However, no pure-play platform exists in our "
        "vertical (supply chain visibility). Analyst reports suggest platform winners "
        "capture 70% of vertical value within 5 years."
    ),
)

SCENARIO_DEFENSIVE_ACQUISITION = StrategyAgentRequest(
    scenario=(
        "A well-funded competitor ($200M Series D) has begun aggressively acquiring "
        "companies in our partner ecosystem. They have acquired 3 integration partners "
        "in 6 months. We are considering a defensive acquisition of our largest "
        "remaining integration partner ($8M ARR, 40 employees, $25M asking price)."
    ),
    context=(
        "The competitor has 3x our revenue and is pursuing a bundling strategy. "
        "If they acquire our top partner, we lose 30% of our implementation channel. "
        "Our current cash position is $40M with $15M annual free cash flow."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_MARKET_ENTRY = StrategyAgentResponse(
    agent_id="strategy",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.7,
    domain_assessment=StrategyDomainAssessment(
        market_opportunity=(
            "Healthcare AI TAM of $12B at 25% CAGR presents a significantly larger "
            "and faster-growing opportunity than our current $8B enterprise analytics "
            "market (15% CAGR). Target's FDA clearances provide 18-24 month regulatory "
            "moat. Realistic SOM: $200-400M within 5 years given our enterprise sales motion."
        ),
        competitive_advantage=(
            "12 patents create defensible IP position. FDA clearances take 18+ months "
            "for competitors to replicate. Combined with our existing AI/ML platform "
            "and enterprise distribution, we would have a unique positioning: regulated "
            "AI + enterprise-grade analytics. However, healthcare domain expertise gap is real."
        ),
        strategic_fit=(
            "Moderate strategic fit. Extends our AI capabilities into a high-value vertical "
            "but requires entirely new go-to-market, regulatory, and domain expertise. "
            "Synergy score: 6/10 — technology synergies are strong but operational synergies are limited."
        ),
        execution_complexity=(
            "High complexity. Healthcare requires regulatory expertise, clinical validation "
            "workflows, and enterprise sales cycles of 12-18 months. Integration risk is "
            "significant given zero healthcare domain experience. Cultural integration of "
            "a 50-person clinical AI team into an enterprise analytics company is non-trivial."
        ),
        strategic_priority=StrategicPriority.HIGH,
    ),
    summary=(
        "Conditionally support the healthcare AI acquisition — the market opportunity "
        "is compelling but execution risk from zero healthcare expertise requires mitigation."
    ),
    rationale=(
        "The strategic rationale for this acquisition is sound: healthcare AI represents a "
        "larger, faster-growing market with higher barriers to entry. The target's FDA "
        "clearances and patent portfolio provide a regulatory moat that would take us 2-3 "
        "years and $10M+ to build organically. The timing is urgent — two competitors "
        "entered last year, and the window for establishing a beachhead is narrowing.\n\n"
        "However, the execution complexity cannot be understated. Healthcare is a regulated "
        "industry requiring domain expertise we do not possess. The acquisition provides the "
        "technology and clearances, but success depends on retaining the target's clinical "
        "team and building healthcare go-to-market capabilities. At 15x ARR ($45M), the "
        "premium is justified only if we can accelerate the target's growth using our "
        "enterprise distribution.\n\n"
        "The key strategic question is whether healthcare AI becomes a core pillar of our "
        "strategy or remains an experiment. If core, the acquisition price is reasonable "
        "for the strategic asset. If experimental, the commitment level is too high and "
        "a partnership or minority investment would be more appropriate."
    ),
    risks=[
        "Healthcare domain expertise gap may prevent effective integration and growth acceleration — target team retention is critical",
        "Competitor response: incumbents with healthcare expertise may acquire alternative targets, closing the window",
        "Strategic dilution: management attention split between core analytics and new healthcare vertical during critical growth phase",
        "Market timing: if healthcare AI adoption slows due to regulatory changes, the premium paid becomes difficult to justify",
    ],
    conditions=[
        "Secure retention agreements with key clinical and technical leaders for minimum 3 years before closing",
        "Validate that our enterprise sales motion can effectively sell to health systems through 3+ pilot conversations",
        "Confirm no material regulatory changes pending that would invalidate FDA clearances within 24 months",
        "Establish dedicated healthcare business unit with autonomous P&L to prevent cultural integration issues",
    ],
    metrics_to_track=[
        "Healthcare revenue as percentage of total — target 15% within 3 years",
        "Key personnel retention rate in acquired team — must remain above 85% for 24 months",
        "New healthcare customer acquisition rate — target 10 health systems in Year 1",
        "Competitive positioning: maintain top-3 ranking in healthcare AI analyst reports",
        "Cross-sell success: percentage of existing customers adopting healthcare modules",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_PLATFORM_PIVOT = StrategyAgentResponse(
    agent_id="strategy",
    round=1,
    position=Position.SUPPORT,
    confidence=0.75,
    domain_assessment=StrategyDomainAssessment(
        market_opportunity=(
            "Platform economics in vertical SaaS show 70% value capture for winners. "
            "In supply chain visibility (our vertical), no platform exists yet — this is "
            "a first-mover opportunity. Platform TAM is estimated 3-5x our current point-solution "
            "TAM as we capture ecosystem economics (marketplace fees, data network effects)."
        ),
        competitive_advantage=(
            "First-mover in vertical platform creates powerful network effects: more integrations "
            "attract more developers, which attract more customers. Our 200 enterprise customers "
            "provide initial demand-side liquidity. No competitor has our combination of "
            "enterprise relationships + vertical depth + technical capability for platform."
        ),
        strategic_fit=(
            "Strong strategic fit — this is a natural evolution from point-solution to platform "
            "that leverages all existing assets (customer base, domain expertise, data assets). "
            "Aligns with board's stated ambition to build a category-defining company."
        ),
        execution_complexity=(
            "Very high complexity. Platform transitions require simultaneous investment in "
            "developer ecosystem, API infrastructure, marketplace operations, and new PLG "
            "go-to-market — all while maintaining enterprise sales for existing customers. "
            "Estimated 24-36 months to reach platform-market fit."
        ),
        strategic_priority=StrategicPriority.CRITICAL,
    ),
    summary=(
        "Support the platform pivot — first-mover advantage in vertical platforms is decisive, "
        "and the window of opportunity will not remain open indefinitely."
    ),
    rationale=(
        "This is a generational strategic decision. Analyst research consistently shows that "
        "in B2B verticals, the platform winner captures 60-70% of total ecosystem value. "
        "No platform exists in supply chain visibility today, creating a rare first-mover "
        "opportunity. Our 200 enterprise customers provide the demand-side foundation that "
        "platform competitors need years to build.\n\n"
        "The risk of inaction is equally significant. If a horizontal platform (Salesforce, "
        "ServiceNow) builds supply chain capabilities, or if a well-funded startup pursues "
        "platform-first in our vertical, our point-solution position becomes indefensible "
        "within 3-5 years. Platform economics make it nearly impossible for point solutions "
        "to compete once a platform achieves critical mass.\n\n"
        "The execution complexity is the primary concern. Platform transitions have a high "
        "failure rate because they require simultaneous investment across multiple dimensions. "
        "I recommend a 'platform-gradual' approach: open APIs to existing partners first, "
        "build marketplace with curated integrations, then expand to open developer ecosystem. "
        "This sequences the investment while building platform capabilities progressively."
    ),
    risks=[
        "Platform transitions have 60%+ failure rate — requires sustained investment over 24-36 months before network effects compound",
        "Existing enterprise customers may resist open platform model if it enables competitors to integrate",
        "Developer ecosystem requires critical mass (50+ integrations) before value proposition becomes self-reinforcing",
        "Horizontal platform players (Salesforce) may enter our vertical before we achieve platform-market fit",
    ],
    conditions=[
        "Secure board commitment to 36-month investment horizon with clear stage gates at 12 and 24 months",
        "Validate developer demand through beta program with minimum 20 integration partners committed",
        "Maintain enterprise customer NPS above 50 throughout transition to prevent core business erosion",
        "Achieve 25+ live marketplace integrations within 18 months as leading indicator of platform viability",
    ],
    metrics_to_track=[
        "Number of active third-party integrations on platform — target 50 within 24 months",
        "Developer ecosystem growth rate — monthly active developers building on platform",
        "Platform revenue as percentage of total (marketplace fees + API usage) — target 20% by Year 3",
        "Enterprise customer retention during transition — must remain above 92%",
        "Time to platform-market fit: developer NPS above 40 and organic integration growth",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Healthcare AI Market Entry", SCENARIO_MARKET_ENTRY),
    ("APAC Geographic Expansion", SCENARIO_GEOGRAPHIC_EXPANSION),
    ("Platform Pivot", SCENARIO_PLATFORM_PIVOT),
    ("Defensive Acquisition", SCENARIO_DEFENSIVE_ACQUISITION),
]

ALL_EXAMPLE_RESPONSES = [
    ("Healthcare AI Market Entry", EXAMPLE_RESPONSE_MARKET_ENTRY),
    ("Platform Pivot", EXAMPLE_RESPONSE_PLATFORM_PIVOT),
]
