"""Marketing Agent example scenarios and expected responses."""

from .schema import (
    MarketingAgentRequest,
    MarketingAgentResponse,
    MarketingDomainAssessment,
    Position,
    BrandImpact,
    CompetitivePosition,
    GoToMarketComplexity,
)

SCENARIO_NEW_PRODUCT_LAUNCH = MarketingAgentRequest(
    scenario=(
        "We are considering launching a new B2B SaaS product targeting mid-market "
        "companies. The product is an AI-powered analytics dashboard priced at "
        "$2,000/month. Our brand is currently known for enterprise solutions."
    ),
    context="Current customer base is 80% enterprise (1000+ employees). We have no mid-market presence.",
)

SCENARIO_REBRAND = MarketingAgentRequest(
    scenario=(
        "The leadership team is considering a full company rebrand including new name, "
        "visual identity, and messaging framework. The current brand has 8 years of equity "
        "but is perceived as 'legacy' by younger buyers entering decision-making roles."
    ),
    context="NPS among customers under 35 is 22 (vs. 58 for customers over 45). Competitor launched fresh brand last quarter.",
)

SCENARIO_MARKET_EXPANSION = MarketingAgentRequest(
    scenario=(
        "Our US-based platform is considering expansion into European markets starting "
        "with UK and Germany. We need localized marketing, local partnerships, and "
        "region-specific content strategy."
    ),
    context="No existing European brand awareness. Competitor has 18-month head start in EU.",
)

SCENARIO_PRICING_CHANGE = MarketingAgentRequest(
    scenario=(
        "The finance team proposes increasing prices by 25% for all new customers while "
        "grandfathering existing customers for 12 months. Current pricing is seen as "
        "'affordable' in the market."
    ),
    context="3 competitors are priced 30-50% higher. Our low price is a key differentiator in sales conversations.",
)

SCENARIO_PARTNERSHIP = MarketingAgentRequest(
    scenario=(
        "A major cloud provider has offered a co-marketing partnership where they would "
        "feature our product in their marketplace and co-fund $500K in joint marketing "
        "campaigns over 12 months."
    ),
    context="The cloud provider serves 40% of our target market. Partnership would require exclusive integration for 18 months.",
)

EXAMPLE_RESPONSE_NEW_PRODUCT = MarketingAgentResponse(
    agent_id="marketing",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.6,
    domain_assessment=MarketingDomainAssessment(
        market_opportunity=(
            "Mid-market B2B analytics TAM estimated at $4.2B globally. SAM for "
            "AI-powered dashboards in our verticals: ~$800M. Achievable SOM in Year 1: "
            "$5-15M given zero current mid-market brand presence."
        ),
        brand_impact=BrandImpact.NEGATIVE,
        competitive_position=CompetitivePosition.UNCHANGED,
        customer_segments_affected=["Mid-market companies (500-2000 employees)", "Existing enterprise customers who may perceive downmarket move"],
        go_to_market_complexity=GoToMarketComplexity.HIGH,
    ),
    summary=(
        "The market opportunity is real but moving downmarket risks diluting our enterprise "
        "brand positioning without a dedicated sub-brand strategy."
    ),
    rationale=(
        "The mid-market analytics space is genuinely attractive — growing at 28% CAGR with "
        "underserved demand for AI-powered tools. However, our brand is built on enterprise "
        "credibility. Moving downmarket without a clear brand architecture strategy risks "
        "confusing both segments: mid-market buyers may see us as 'too expensive and complex' "
        "while enterprise buyers may question our focus.\n\n"
        "Competitors like Mixpanel and Amplitude have demonstrated that mid-market SaaS "
        "analytics can scale effectively, but they built from that segment upward. We would "
        "be moving in the opposite direction, which requires different messaging, different "
        "channels (product-led growth vs. enterprise sales), and potentially different brand "
        "identity.\n\n"
        "I recommend a sub-brand or 'powered by' approach that captures mid-market demand "
        "without diluting the parent brand. This adds GTM complexity but protects our core "
        "positioning. Without this, I expect brand confusion within 6-12 months."
    ),
    risks=[
        "Brand dilution among enterprise customers who value exclusivity and perceive mid-market as 'downgrade'",
        "Channel conflict: mid-market requires PLG/self-serve but our entire GTM is enterprise sales-led",
        "Messaging confusion: one brand cannot credibly promise both 'enterprise-grade' and 'accessible for growing teams'",
        "Competitive response: mid-market incumbents will position against us as 'overpriced enterprise tool'",
    ],
    conditions=[
        "Develop sub-brand strategy before launch — separate identity that borrows but doesn't dilute parent brand",
        "Validate mid-market messaging with 20+ target buyer interviews before committing to positioning",
        "Allocate dedicated marketing budget ($200K+) for mid-market — do not cannibalize enterprise marketing spend",
        "Establish clear brand architecture guidelines that define relationship between enterprise and mid-market offerings",
    ],
    recommended_actions=[
        "Commission brand architecture study to define sub-brand vs. product-line approach",
        "Run positioning research with mid-market buyers to validate willingness-to-pay and key messages",
        "Develop separate landing page and content strategy for mid-market — test with paid acquisition before full launch",
        "Create internal brand guidelines that prevent enterprise messaging contamination",
    ],
    references_to=[],
)

ALL_SCENARIOS = [
    ("New Product Launch", SCENARIO_NEW_PRODUCT_LAUNCH),
    ("Company Rebrand", SCENARIO_REBRAND),
    ("European Market Expansion", SCENARIO_MARKET_EXPANSION),
    ("Pricing Change", SCENARIO_PRICING_CHANGE),
    ("Cloud Partnership", SCENARIO_PARTNERSHIP),
]

ALL_EXAMPLE_RESPONSES = [
    ("New Product Launch", EXAMPLE_RESPONSE_NEW_PRODUCT),
]
