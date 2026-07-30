"""Product Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Product Agent's output quality
2. Demonstrating the expected style of product reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    ProductAgentRequest,
    ProductAgentResponse,
    ProductDomainAssessment,
    Position,
    Feasibility,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_COLLABORATION_FEATURE = ProductAgentRequest(
    scenario=(
        "We are considering adding real-time collaboration features (multiplayer editing, "
        "live cursors, commenting) to our project management tool. User research shows "
        "35% of churned users cited 'lack of collaboration' as a reason for leaving. "
        "Competitors Notion, Monday.com, and Linear all launched real-time features in 2024."
    ),
    context=(
        "Current DAU: 45K. NPS: 42. Feature requests for collaboration: #1 on our public "
        "roadmap (800+ votes). Average workspace size: 8 users. Current engagement: "
        "2.3 sessions/day per user."
    ),
)

SCENARIO_MOBILE_APP = ProductAgentRequest(
    scenario=(
        "The sales team is requesting a native mobile app (iOS + Android) for our B2B "
        "analytics platform. Currently we only have a responsive web app. Three enterprise "
        "prospects ($500K+ ACV) have listed mobile as a requirement in their RFPs."
    ),
    context=(
        "Current mobile web traffic: 12% of total. Competitor mobile app ratings: "
        "Competitor A (4.2★, 5K reviews), Competitor B (3.8★, 2K reviews). "
        "Engineering estimate: 6 months for MVP with 2 dedicated mobile engineers."
    ),
)

SCENARIO_AI_ASSISTANT = ProductAgentRequest(
    scenario=(
        "We want to add an AI-powered assistant to our customer support platform that "
        "can auto-resolve tier-1 tickets. The goal is to reduce average resolution time "
        "from 4 hours to under 15 minutes for common issues. We have 2 years of "
        "historical ticket data (500K+ tickets) to train on."
    ),
    context=(
        "Current tier-1 ticket volume: 3,000/month. Agent cost per ticket: $12. "
        "Customer satisfaction for human-resolved tickets: 4.1/5. Top 10 issue "
        "categories cover 70% of tier-1 volume. Beta test with 50 customers showed "
        "65% auto-resolution rate with 4.0/5 satisfaction."
    ),
)

SCENARIO_PLATFORM_REDESIGN = ProductAgentRequest(
    scenario=(
        "We are proposing a full UI/UX redesign of our 5-year-old SaaS platform. "
        "The current interface has accumulated design debt: inconsistent patterns, "
        "nested navigation up to 5 levels deep, and 23 different modal types. "
        "New user onboarding takes an average of 14 days to first value."
    ),
    context=(
        "NPS: 31 (down from 45 two years ago). Primary NPS detractor theme: 'hard to use'. "
        "Competitor NPS scores: 55-65 range. Time-to-value for competitors: 2-5 days. "
        "40% of support tickets are 'how do I do X' questions."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_COLLABORATION = ProductAgentResponse(
    agent_id="product",
    round=1,
    position=Position.SUPPORT,
    confidence=0.82,
    domain_assessment=ProductDomainAssessment(
        product_market_fit=(
            "Strong PMF signals across multiple vectors: 35% churn exit-survey correlation, "
            "#1 requested feature (800+ votes), and all major competitors have shipped similar "
            "capabilities. The absence of collaboration is now a competitive disadvantage rather "
            "than an optional enhancement. Market has spoken clearly."
        ),
        roadmap_impact=(
            "Significant roadmap commitment: estimated 3-4 engineering sprints (6-8 weeks) for "
            "core multiplayer infrastructure, plus 4-6 weeks for commenting and presence features. "
            "Displaces planned workflow automation features from Q3. Trade-off is justified given "
            "the 35% churn correlation — retention features should outprioritize expansion features."
        ),
        user_experience=(
            "Collaboration features transform the product from single-player to multiplayer. "
            "User journey shifts from 'create-share-wait' to 'create-together'. Expected "
            "improvements: activation rate +20% (teams adopt faster when they can collaborate), "
            "session frequency +30% (more reasons to return). Design challenge: ensuring "
            "collaboration doesn't add noise for solo users."
        ),
        build_vs_buy=(
            "Build core infrastructure (CRDT/OT engine) using open-source foundation (Yjs). "
            "Buy: real-time cursor library (Liveblocks or similar) for accelerated delivery. "
            "Partner: integrate with existing commenting tools (Loom for video comments). "
            "Hybrid approach delivers 70% of value in 50% of build time."
        ),
        feasibility=Feasibility.COMPLEX,
    ),
    summary=(
        "Strongly support real-time collaboration — validated user demand, clear competitive "
        "necessity, and direct correlation to our #1 retention challenge."
    ),
    rationale=(
        "The product case for real-time collaboration is overwhelming. Three independent data "
        "points converge: 35% of churned users cite collaboration as the gap, it's our #1 "
        "requested feature with 800+ votes, and every meaningful competitor now offers it. "
        "We are losing deals and users to a capability gap that the market has clearly defined.\n\n"
        "From a roadmap perspective, this should be our top priority even at the cost of "
        "delaying planned features. The logic is straightforward: retention-improving features "
        "have higher compound value than expansion features because they protect the base "
        "revenue that funds future development. A 35% churn correlation suggests we're "
        "leaving significant LTV on the table every month we delay.\n\n"
        "The feasibility is complex but manageable. Using Yjs (CRDT library) as infrastructure "
        "and Liveblocks-style cursor presence, we can ship a meaningful V1 in 8-10 weeks "
        "that includes co-editing and presence. Comments and reactions follow in V2. The key "
        "design principle: collaboration should enhance the solo experience, never degrade it."
    ),
    risks=[
        "Real-time infrastructure adds significant technical surface area — operational reliability must match or exceed current uptime",
        "Collaboration features can increase product complexity for solo users if not designed with progressive disclosure",
        "Competitive catch-up: we're late to market and initial version may feel inferior to mature competitor implementations",
        "User migration: existing power users may resist workflow changes required to support real-time editing",
    ],
    conditions=[
        "Validate V1 scope with 10 customer design partners before committing full engineering sprint",
        "Achieve 99.9% uptime on collaboration infrastructure during 4-week beta before GA launch",
        "Solo-user experience must not degrade — measure via A/B test showing zero negative impact on solo metrics",
        "Beta NPS for collaboration features must reach 50+ before full rollout",
    ],
    metrics_to_track=[
        "Collaboration adoption: % of workspaces with 2+ active editors — target 60% within 90 days",
        "Churn rate impact: track 'collaboration' exit-survey responses — target reduction from 35% to below 15%",
        "Session frequency: average daily sessions per user — target increase from 2.3 to 3.0",
        "Time-to-value for new teams: target reduction from 14 days to 7 days",
        "Real-time infrastructure reliability: P99 latency below 200ms, uptime above 99.9%",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_AI_ASSISTANT = ProductAgentResponse(
    agent_id="product",
    round=1,
    position=Position.SUPPORT,
    confidence=0.78,
    domain_assessment=ProductDomainAssessment(
        product_market_fit=(
            "Strong validation from beta results: 65% auto-resolution rate with 4.0/5 "
            "satisfaction matches human performance (4.1/5). The 3,000 monthly tier-1 tickets "
            "represent clear demand for faster resolution. Market is rapidly adopting AI support "
            "(Intercom, Zendesk, Freshdesk all launched AI features in 2024)."
        ),
        roadmap_impact=(
            "Moderate roadmap impact. Core ML infrastructure already exists from beta. "
            "GA readiness requires: edge case handling, confidence thresholds, human "
            "handoff UX, and admin controls. Estimated 8-10 weeks incremental work. "
            "Does not significantly displace other planned features."
        ),
        user_experience=(
            "Transforms support experience from 'submit-and-wait-4-hours' to 'instant-resolution'. "
            "Critical UX requirement: transparency about AI vs. human, easy escalation path, "
            "and confidence indicators. Poor UX here erodes trust in entire platform."
        ),
        build_vs_buy=(
            "Build — we have unique advantage with 500K historical tickets providing "
            "domain-specific training data no vendor can match. Generic AI support tools "
            "achieve 30-40% resolution; our 65% beta result validates the build approach."
        ),
        feasibility=Feasibility.MODERATE,
    ),
    summary=(
        "Support AI assistant launch — beta results validate strong product-market fit "
        "with 65% resolution rate matching human satisfaction scores."
    ),
    rationale=(
        "The beta results make a compelling product case: 65% auto-resolution with 4.0/5 "
        "satisfaction versus 4.1/5 for human agents demonstrates that AI can handle the "
        "majority of tier-1 volume without degrading the customer experience. This is rare "
        "— most AI support implementations fail on satisfaction scores.\n\n"
        "The product differentiator is our 500K-ticket training dataset. This gives us "
        "domain-specific performance that no horizontal AI support vendor can match. The "
        "65% vs. industry-average 30-40% resolution rate is directly attributable to this "
        "proprietary data advantage. This is a defensible product moat.\n\n"
        "The critical product risk is trust. Users must feel confident in AI responses and "
        "have friction-free escalation to humans. The UX must clearly communicate AI "
        "confidence levels and never present uncertain answers as definitive. Progressive "
        "rollout starting with highest-confidence issue categories will build trust gradually."
    ),
    risks=[
        "AI confidence miscalibration could auto-resolve tickets incorrectly, damaging customer trust in entire support experience",
        "Edge cases in the 35% non-auto-resolved tickets may create frustrating loops before human handoff",
        "Customer perception risk: users may feel 'stuck with a bot' even when AI provides correct answers",
        "Training data drift: as product evolves, historical tickets become less relevant without continuous retraining",
    ],
    conditions=[
        "Maintain satisfaction score above 3.8/5 for AI-resolved tickets at GA scale (not just beta cohort)",
        "Human escalation must be available within 1 click, with full context transfer (no re-explanation)",
        "Auto-resolution confidence threshold must be set at 90%+ to prevent false positives",
        "Weekly model monitoring with automatic fallback to human routing if resolution satisfaction drops below 3.5/5",
    ],
    metrics_to_track=[
        "Auto-resolution rate by issue category — overall target 65%, expand categories monthly",
        "AI-resolved ticket satisfaction score — maintain parity with human (4.0+/5)",
        "Escalation rate and post-escalation satisfaction — target smooth handoff experience",
        "Mean time to resolution: AI path vs. human path — target 15 min vs. 4 hour baseline",
        "Support cost per ticket — track reduction from $12 baseline as AI handles more volume",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Real-Time Collaboration", SCENARIO_COLLABORATION_FEATURE),
    ("Native Mobile App", SCENARIO_MOBILE_APP),
    ("AI Support Assistant", SCENARIO_AI_ASSISTANT),
    ("Platform UI Redesign", SCENARIO_PLATFORM_REDESIGN),
]

ALL_EXAMPLE_RESPONSES = [
    ("Real-Time Collaboration", EXAMPLE_RESPONSE_COLLABORATION),
    ("AI Support Assistant", EXAMPLE_RESPONSE_AI_ASSISTANT),
]
