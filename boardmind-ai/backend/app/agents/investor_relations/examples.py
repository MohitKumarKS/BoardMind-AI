"""Investor Relations Officer example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Investor Relations Agent's output quality
2. Demonstrating the expected style of IR reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    InvestorRelationsAgentRequest,
    InvestorRelationsAgentResponse,
    InvestorRelationsDomainAssessment,
    Position,
    InvestorSentiment,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_MAJOR_ACQUISITION = InvestorRelationsAgentRequest(
    scenario=(
        "We are considering acquiring a competitor for $2.1B, funded 60% cash and "
        "40% stock issuance. The target has $400M revenue growing 25% YoY with "
        "negative EBITDA of -$50M. The acquisition would make us the market leader "
        "but dilute existing shareholders by approximately 12%."
    ),
    context=(
        "Our current market cap: $8.5B. Revenue: $1.2B growing 18% YoY. EBITDA margin: 22%. "
        "Top 10 institutional holders own 58% of shares. Last acquisition (3 years ago) "
        "resulted in 15% stock decline over 60 days before recovering. Activist investor "
        "holds 4.2% stake and has publicly advocated for 'disciplined capital allocation'."
    ),
)

SCENARIO_EARNINGS_MISS = InvestorRelationsAgentRequest(
    scenario=(
        "Preliminary Q3 results show revenue of $298M vs. consensus of $315M (5.4% miss) "
        "and EPS of $0.72 vs. consensus of $0.85 (15.3% miss). The shortfall is due to "
        "delayed enterprise deals that are expected to close in Q4. We need to decide "
        "how to communicate this to the market."
    ),
    context=(
        "We raised guidance last quarter with confidence. Two sell-side analysts have "
        "the stock as their top pick. Short interest has increased 40% in the last month "
        "(suggesting some anticipated weakness). Our track record: beat consensus 8 of "
        "last 10 quarters. Pre-announcement would be 2 weeks before regular earnings date."
    ),
)

SCENARIO_SHARE_BUYBACK = InvestorRelationsAgentRequest(
    scenario=(
        "The board is considering authorizing a $500M accelerated share repurchase (ASR) "
        "program, representing approximately 6% of current market cap. This would be our "
        "largest buyback ever and would be funded from cash reserves and a $200M term loan. "
        "The decision was prompted by management's belief that shares are undervalued by 25-30%."
    ),
    context=(
        "Current share price: $45 (52-week high: $72, low: $38). Forward P/E: 14x vs. "
        "peer average 19x. Cash on hand: $800M. Net debt/EBITDA: 1.2x (would increase to 1.8x). "
        "Dividend yield: 2.1%. Three activist funds have accumulated positions totaling 8% "
        "in the last 90 days."
    ),
)

SCENARIO_STRATEGIC_PIVOT = InvestorRelationsAgentRequest(
    scenario=(
        "The CEO plans to announce a strategic pivot from our legacy hardware business "
        "(60% of revenue, declining 5% YoY) to a cloud-based subscription model. The "
        "transition will take 3 years, with revenue declining 15-20% in Year 1 before "
        "recovering. The announcement will include a restructuring charge of $180M."
    ),
    context=(
        "Current revenue mix: 60% hardware ($720M), 40% services/subscription ($480M). "
        "Subscription growing 35% YoY. Hardware peer multiples: 8-12x earnings. "
        "SaaS peer multiples: 25-40x earnings. Three board members from legacy hardware "
        "era. 45% of institutional base are value investors attracted by hardware margins."
    ),
)

SCENARIO_ESG_CONTROVERSY = InvestorRelationsAgentRequest(
    scenario=(
        "An investigative journalist is preparing to publish a story alleging our supply "
        "chain uses forced labor in two overseas facilities. Our compliance team has "
        "confirmed some audit gaps but no confirmed violations. The story is expected "
        "to publish in 5 days. ESG-focused funds hold 22% of our shares."
    ),
    context=(
        "ESG rating: MSCI A (industry average: BBB). 3 ESG-focused ETFs hold our stock. "
        "Peer company faced similar allegation last year and lost 18% market cap in 2 weeks "
        "before partial recovery. Our supply chain audit coverage: 78% of tier-1 suppliers, "
        "35% of tier-2. No previous labor practice controversies."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_ACQUISITION = InvestorRelationsAgentResponse(
    agent_id="investor_relations",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.6,
    domain_assessment=InvestorRelationsDomainAssessment(
        market_perception=(
            "Mixed-to-negative initial reaction expected. 12% dilution from stock issuance "
            "will concern existing holders. Negative EBITDA target at $2.1B valuation "
            "(5.25x revenue) will face scrutiny on valuation discipline. Activist investor "
            "(4.2% stake) likely to publicly oppose. Positive offset: market leadership "
            "narrative and 25% target growth rate. Historical precedent: our last acquisition "
            "caused 15% decline before recovery — similar pattern likely."
        ),
        earnings_impact=(
            "Immediate EPS dilution of $0.15-0.20 from share issuance and target's "
            "negative EBITDA. Accretive timeline: 18-24 months assuming synergy capture "
            "of $80-120M. GAAP earnings will show amortization drag of ~$0.08/share "
            "for 5+ years. Non-GAAP adjusted EPS accretive by Q6-Q8 post-close. "
            "Full-year guidance must be reset — consensus will need to rebuild."
        ),
        shareholder_value=(
            "Long-term value creation potential of 20-35% if synergies are realized and "
            "combined entity achieves market leader premium. Near-term value destruction "
            "risk of 10-20% from dilution, integration uncertainty, and multiple compression. "
            "Market leader position historically commands 2-4x multiple premium in our sector. "
            "Risk: paying 5.25x revenue for money-losing business creates 'winner's curse' narrative."
        ),
        communication_strategy=(
            "Critical: pre-brief activist investor and top 5 holders before announcement. "
            "Frame as 'generational market leadership opportunity' not 'growth acquisition'. "
            "Lead with synergy detail and path to accretion. Announce simultaneous cost "
            "synergy targets ($80-120M by Year 2) to offset dilution narrative. Host "
            "analyst/investor day within 48 hours of announcement with detailed integration "
            "plan. CEO and CFO joint availability for 1:1 calls with top 20 holders."
        ),
        investor_sentiment=InvestorSentiment.MIXED,
    ),
    summary=(
        "Conditionally support — acquisition can create value but requires exceptional "
        "communication execution to manage 12% dilution narrative and activist opposition."
    ),
    rationale=(
        "This acquisition presents a significant investor relations challenge. The 12% "
        "dilution, combined with a money-losing target at 5.25x revenue multiple, will "
        "strain management credibility with value-oriented holders. Our experience with "
        "the previous acquisition (15% stock decline over 60 days) provides a realistic "
        "template for market reaction. The activist investor (4.2%) will almost certainly "
        "use this as a catalyst for public opposition, which amplifies negative sentiment.\n\n"
        "However, the strategic narrative is defensible: market leadership with 25% growth "
        "target at a time when our organic growth is 18% creates a compelling combination "
        "story. The key is leading with specific synergy targets and an accretion timeline "
        "that gives analysts something concrete to model. Without specific numbers, the "
        "market will default to skepticism about 'strategic value' claims.\n\n"
        "The communication strategy is the decisive factor. Pre-briefing major holders "
        "is essential — the worst outcome is institutional holders learning about 12% "
        "dilution from a press release. The 48-hour window between leak risk and "
        "announcement must be managed carefully. I recommend Monday morning announcement "
        "to give a full trading week for analyst updates and investor calls, avoiding "
        "the Friday afternoon 'bad news dump' perception."
    ),
    risks=[
        "Activist investor (4.2% stake) likely to launch public campaign against acquisition — 'capital allocation discipline' narrative ready-made",
        "12% dilution triggers automatic selling from index funds with concentration limits and value-oriented holders with dilution constraints",
        "Integration execution risk amplified in public markets — any missed synergy milestone will be treated as confirmation of overpayment",
        "Consensus estimate reset creates 'beat and raise' gap — may take 3-4 quarters to rebuild analyst confidence in guidance credibility",
    ],
    conditions=[
        "Pre-brief activist investor with detailed synergy plan and governance commitments before public announcement",
        "Announce specific, measurable synergy targets ($80-120M) with quarterly milestone reporting commitment",
        "Schedule analyst/investor day within 48 hours of announcement with CFO-led integration financial model",
        "Prepare proxy defense materials in case activist escalates to board challenge or 'vote no' campaign",
    ],
    metrics_to_track=[
        "Stock price performance vs. sector index — 7, 30, 60, 90 day windows post-announcement",
        "Institutional ownership changes — weekly 13F/13D filing monitoring for position reductions",
        "Analyst recommendation changes and price target revisions within 30 days",
        "Synergy realization vs. stated targets — quarterly reporting to investment community",
        "Integration milestone achievement — public scorecard for investor accountability",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_BUYBACK = InvestorRelationsAgentResponse(
    agent_id="investor_relations",
    round=1,
    position=Position.SUPPORT,
    confidence=0.8,
    domain_assessment=InvestorRelationsDomainAssessment(
        market_perception=(
            "Strongly positive expected reaction. $500M ASR at current valuation (14x P/E "
            "vs. 19x peer average) signals management conviction in undervaluation. "
            "Activist accumulation (8% in 90 days) suggests market already expects "
            "capital return action — this satisfies that pressure constructively. "
            "Largest-ever buyback demonstrates seriousness of undervaluation view."
        ),
        earnings_impact=(
            "Immediate mechanical EPS accretion of ~6% from share count reduction. "
            "At $45/share, approximately 11.1M shares retired. Interest expense from "
            "$200M term loan: ~$12M/year ($0.05/share drag). Net EPS accretion: ~5.5%. "
            "Pro forma forward P/E compresses from 14x to ~13.3x, making valuation gap "
            "more visible. No impact on revenue or operating income."
        ),
        shareholder_value=(
            "Strong value creation if management's 25-30% undervaluation thesis is correct. "
            "At $45 purchase with fair value of $58-62, implied return on buyback capital "
            "of 29-38%. Even at 15% undervaluation, buyback outperforms alternative uses "
            "of capital at current rates. Net debt/EBITDA at 1.8x remains conservative "
            "for investment-grade credit. Maintains dividend capacity."
        ),
        communication_strategy=(
            "Announce alongside Q-result or separately with 8-K filing. Frame as 'management "
            "putting money where conviction is' — emphasize insiders not selling. Reference "
            "valuation gap to peers (14x vs. 19x). Pre-brief top holders — this is good news "
            "but size ($500M, largest ever) warrants preparation. Include board authorization "
            "quote emphasizing confidence in long-term value. Consider coupling with updated "
            "capital allocation framework presentation."
        ),
        investor_sentiment=InvestorSentiment.POSITIVE,
    ),
    summary=(
        "Strongly support — $500M ASR at current discount to peers signals management "
        "conviction, addresses activist pressure, and creates immediate EPS accretion."
    ),
    rationale=(
        "This is a textbook investor relations positive: a large-scale buyback at a "
        "significant discount to intrinsic value and peer multiples. The market will "
        "interpret the $500M commitment (largest ever) as a strong signal of management "
        "confidence. The 14x vs. 19x peer gap provides objective support for the "
        "undervaluation thesis that analysts can independently verify.\n\n"
        "The timing is also favorable from an IR perspective. Activist accumulation "
        "(8% in 90 days) creates implicit pressure for capital return. By acting "
        "proactively rather than reactively, management maintains strategic initiative "
        "and can frame the buyback as part of a deliberate capital allocation philosophy "
        "rather than a response to activist demands. This preserves management "
        "credibility and narrative control.\n\n"
        "The balance sheet impact is manageable — 1.8x net debt/EBITDA remains well "
        "within investment-grade parameters and does not jeopardize the dividend. "
        "The key risk is if the stock continues to decline post-announcement, creating "
        "a 'catching a falling knife' narrative. However, the activist presence likely "
        "creates a floor, and the mechanical EPS accretion provides immediate tangible "
        "benefit regardless of near-term price action."
    ),
    risks=[
        "Stock price decline post-buyback creates 'value trap' narrative — board looks wrong if shares fall further below $38 low",
        "Leverage increase to 1.8x may concern fixed-income investors and could trigger credit rating review commentary",
        "If business deteriorates, buyback will be criticized as 'financial engineering' masking operational weakness",
        "Activist may argue $500M is insufficient and push for larger return — sets precedent for escalating demands",
    ],
    conditions=[
        "Announce with clear capital allocation framework showing buyback as part of disciplined strategy, not one-time event",
        "Ensure executive team is not selling shares during or immediately after ASR period — alignment signal is critical",
        "Prepare response for credit rating agency inquiries regarding leverage increase to 1.8x",
        "Establish completion timeline disclosure — update market quarterly on ASR progress and remaining authorization",
    ],
    metrics_to_track=[
        "Average purchase price vs. subsequent share price — demonstrate buyback value creation",
        "EPS accretion realized vs. projected — report quarterly to validate capital allocation thesis",
        "Peer valuation gap — track our P/E multiple convergence toward 19x peer average",
        "Institutional ownership quality — monitor for upgrade from value to GARP/growth holders",
        "Activist position changes — monitor 13D/13F filings for accumulation or exit signals",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Major Acquisition", SCENARIO_MAJOR_ACQUISITION),
    ("Earnings Miss", SCENARIO_EARNINGS_MISS),
    ("Share Buyback", SCENARIO_SHARE_BUYBACK),
    ("Strategic Pivot", SCENARIO_STRATEGIC_PIVOT),
    ("ESG Controversy", SCENARIO_ESG_CONTROVERSY),
]

ALL_EXAMPLE_RESPONSES = [
    ("Major Acquisition", EXAMPLE_RESPONSE_ACQUISITION),
    ("Share Buyback", EXAMPLE_RESPONSE_BUYBACK),
]
