"""ESG & Sustainability Officer example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the ESG Agent's output quality
2. Demonstrating the expected style of sustainability reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    ESGAgentRequest,
    ESGAgentResponse,
    ESGDomainAssessment,
    Position,
    ESGRiskLevel,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_DATA_CENTER_EXPANSION = ESGAgentRequest(
    scenario=(
        "We are planning to build a new hyperscale data center to support our "
        "growing cloud services division. The facility will require approximately "
        "50 MW of power capacity, with projected annual energy consumption of "
        "380 GWh. Location options include regions with varying renewable energy "
        "availability."
    ),
    context=(
        "Current data center portfolio consumes 120 GWh annually. Company has committed "
        "to net-zero by 2030. Current renewable energy mix is 65%. The new facility would "
        "increase total energy consumption by 316%."
    ),
)

SCENARIO_SUPPLY_CHAIN_RESHORING = ESGAgentRequest(
    scenario=(
        "Our supply chain team proposes reshoring manufacturing from Southeast Asia "
        "back to domestic facilities. This would reduce shipping emissions but increase "
        "production energy costs due to less favorable energy mix. The transition would "
        "affect 2,000 overseas workers and create 800 domestic jobs."
    ),
    context=(
        "Current overseas operations have faced labor practice concerns in third-party audits. "
        "Domestic energy grid is 40% renewable vs. 15% at current overseas locations. "
        "Shipping currently accounts for 12% of our Scope 3 emissions."
    ),
)

SCENARIO_CARBON_CREDIT_PROGRAM = ESGAgentRequest(
    scenario=(
        "The sustainability team proposes launching an internal carbon pricing mechanism "
        "at $85/tonne CO2e, applied to all business units. Revenue generated would fund "
        "renewable energy procurement and nature-based carbon removal projects. "
        "Estimated internal carbon price revenue: $12M annually."
    ),
    context=(
        "Current annual emissions: 142,000 tonnes CO2e. Industry peers have implemented "
        "internal carbon prices ranging from $40-$150/tonne. Board has expressed concern "
        "about competitiveness impact. 60% of emissions come from two business units."
    ),
)

SCENARIO_PACKAGING_TRANSITION = ESGAgentRequest(
    scenario=(
        "Product team proposes transitioning all packaging to 100% recycled and "
        "biodegradable materials within 18 months. Current packaging is 30% recycled "
        "content. The transition requires new supplier relationships and may increase "
        "per-unit packaging cost by 15-25%."
    ),
    context=(
        "Annual packaging spend: $8M. Consumer surveys show 72% preference for sustainable "
        "packaging. Two competitors have already announced similar transitions. Current "
        "packaging generates 3,200 tonnes of plastic waste annually."
    ),
)

SCENARIO_DEI_INITIATIVE = ESGAgentRequest(
    scenario=(
        "HR proposes a comprehensive DEI transformation program including mandatory "
        "unconscious bias training, diverse hiring targets (40% underrepresented groups "
        "for all new hires), supplier diversity requirements (25% spend with minority-owned "
        "businesses), and public DEI reporting with third-party verification."
    ),
    context=(
        "Current workforce: 22% underrepresented groups (industry average: 31%). "
        "Supplier diversity: 8% of spend (peer average: 18%). No current public DEI "
        "reporting. ESG rating agencies have flagged social metrics as area for improvement."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_DATA_CENTER = ESGAgentResponse(
    agent_id="esg",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.7,
    domain_assessment=ESGDomainAssessment(
        environmental_impact=(
            "Projected 170,000 tonnes CO2e annual emissions at current grid mix (45% renewable). "
            "Water consumption estimated at 1.2 billion liters/year for cooling. "
            "Land use: 40 acres including buffer zones. E-waste generation from hardware "
            "refresh cycles estimated at 200 tonnes over 5-year lifecycle."
        ),
        social_impact=(
            "Positive: 300-500 direct jobs, predominantly technical roles. Community "
            "benefit through local tax revenue ($4-6M annually). Concerns: water competition "
            "with agricultural users in drought-prone regions. Digital divide considerations "
            "if facility does not include community connectivity programs."
        ),
        governance_implications=(
            "Requires board ESG committee approval given scale of emissions impact. "
            "Must integrate into existing TCFD climate risk reporting. Executive "
            "compensation ESG targets must account for new facility emissions. "
            "Third-party sustainability audit required pre- and post-construction."
        ),
        sustainability_score=(
            "Current proposal: partial alignment with GRI 302 (Energy) and 305 (Emissions). "
            "TCFD gap: transition risk from potential carbon pricing not modeled. "
            "SASB Technology & Communications standard requires energy management disclosure. "
            "Misalignment with Science Based Targets initiative 1.5°C pathway without 100% renewable commitment."
        ),
        esg_risk=ESGRiskLevel.HIGH,
    ),
    summary=(
        "Conditionally support — the data center expansion must commit to 100% renewable "
        "energy procurement and water stewardship to align with net-zero commitments."
    ),
    rationale=(
        "The proposed data center expansion represents the single largest potential increase "
        "in our environmental footprint. At 380 GWh annual consumption, it would more than "
        "triple our current energy use. Without 100% renewable energy procurement, this "
        "facility alone would generate emissions incompatible with our 2030 net-zero target.\n\n"
        "However, the business need is legitimate, and data center infrastructure can be "
        "built sustainably. Leading peers have demonstrated that hyperscale facilities can "
        "operate at or near 100% renewable energy through a combination of on-site generation, "
        "PPAs, and renewable energy certificates. The key condition is that renewable energy "
        "procurement must be contractually committed before construction, not retrofitted.\n\n"
        "The water consumption presents a secondary but significant environmental concern. "
        "1.2 billion liters annually requires careful site selection to avoid watershed stress. "
        "I recommend sites with water-positive commitments including aquifer replenishment "
        "programs. The governance framework must include quarterly ESG reporting on energy "
        "source, water usage, and emissions with board-level accountability."
    ),
    risks=[
        "Net-zero 2030 target becomes unreachable if facility operates on fossil-heavy grid — 170K tonnes CO2e would exceed remaining carbon budget",
        "Water stress risk in potential locations could trigger community opposition and regulatory intervention",
        "Greenwashing exposure if renewable energy claims rely solely on unbundled RECs rather than additionality-verified PPAs",
        "TCFD reporting gap: climate transition risk from potential $85+/tonne carbon pricing not modeled in facility economics",
    ],
    conditions=[
        "Commit to 100% renewable energy procurement (PPAs or on-site) before construction authorization",
        "Complete water stress assessment for all candidate sites using WRI Aqueduct framework",
        "Establish water-positive commitment with measurable replenishment targets",
        "Integrate facility emissions into Science Based Targets pathway model and confirm alignment",
    ],
    metrics_to_track=[
        "Power Usage Effectiveness (PUE) — target below 1.2",
        "Renewable energy percentage — target 100% within 12 months of operation",
        "Water Usage Effectiveness (WUE) — benchmark against industry leaders",
        "Scope 1 and 2 emissions from facility — monthly tracking against carbon budget",
        "Community impact score — annual third-party assessment",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_CARBON_CREDIT = ESGAgentResponse(
    agent_id="esg",
    round=1,
    position=Position.SUPPORT,
    confidence=0.8,
    domain_assessment=ESGDomainAssessment(
        environmental_impact=(
            "Internal carbon pricing at $85/tonne directly incentivizes 142,000 tonnes CO2e "
            "reduction across business units. Projected 15-25% emissions reduction in Year 1 "
            "from behavioral change alone. $12M revenue funds verified removal projects."
        ),
        social_impact=(
            "Positive signal to employees and stakeholders on climate commitment. "
            "May disproportionately impact carbon-intensive business units (60% of emissions "
            "from two units) — requires just transition support. Green job creation through "
            "funded renewable energy projects."
        ),
        governance_implications=(
            "Demonstrates board-level climate governance leadership. Aligns executive "
            "incentives with decarbonization. Transparent carbon accounting required across "
            "all business units. Sets precedent for Scope 3 supplier engagement."
        ),
        sustainability_score=(
            "Strong alignment with TCFD governance and strategy pillars. Supports GRI 305 "
            "emissions management approach. Exceeds SASB minimum disclosure requirements. "
            "Positions company favorably for CDP A-list consideration. Aligns with "
            "UN SDG 13 (Climate Action)."
        ),
        esg_risk=ESGRiskLevel.LOW,
    ),
    summary=(
        "Strongly support internal carbon pricing — it operationalizes our climate "
        "commitment with measurable accountability and funds verified removal."
    ),
    rationale=(
        "Internal carbon pricing is the single most effective governance mechanism for "
        "driving decarbonization at enterprise scale. At $85/tonne, the price signal is "
        "meaningful enough to change investment decisions while remaining within the range "
        "established by industry peers ($40-$150/tonne). The revenue generated ($12M) "
        "provides substantial funding for high-quality removal projects.\n\n"
        "From a governance perspective, this mechanism embeds climate accountability into "
        "business unit P&Ls, creating natural incentives for efficiency improvements and "
        "clean energy transition. The two business units responsible for 60% of emissions "
        "will face the strongest financial signal, which appropriately concentrates "
        "decarbonization effort where impact is greatest.\n\n"
        "The key to success is ensuring the carbon price revenue funds verified, additional "
        "removal — not low-quality offsets. I recommend allocating at least 50% to "
        "engineered removal (DAC, enhanced weathering) and requiring all nature-based "
        "projects to meet Verra VCS or Gold Standard certification. This protects against "
        "greenwashing risk and ensures genuine atmospheric benefit."
    ),
    risks=[
        "Competitiveness concern if carbon cost is not paired with efficiency support — business units may resist without transition resources",
        "Carbon credit quality risk — if funded projects lack additionality verification, entire program faces greenwashing accusations",
        "Scope boundary disputes between business units could undermine carbon accounting credibility",
        "Regulatory overlap risk if jurisdictional carbon pricing is implemented — must design for compatibility",
    ],
    conditions=[
        "Establish independent carbon accounting verification with annual third-party audit",
        "Allocate minimum 50% of carbon revenue to verified engineered removal projects",
        "Provide transition support budget for high-emission business units in Year 1",
        "Design program to be compatible with potential regulatory carbon pricing mechanisms",
    ],
    metrics_to_track=[
        "Total emissions reduction attributable to carbon price signal — annual measurement",
        "Carbon revenue allocation: percentage to removal vs. reduction vs. avoidance",
        "Removal project verification status — target 100% third-party certified",
        "Business unit emissions intensity trend — quarterly tracking",
        "CDP and ESG rating score changes — annual benchmarking",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Data Center Expansion", SCENARIO_DATA_CENTER_EXPANSION),
    ("Supply Chain Reshoring", SCENARIO_SUPPLY_CHAIN_RESHORING),
    ("Carbon Credit Program", SCENARIO_CARBON_CREDIT_PROGRAM),
    ("Packaging Transition", SCENARIO_PACKAGING_TRANSITION),
    ("DEI Initiative", SCENARIO_DEI_INITIATIVE),
]

ALL_EXAMPLE_RESPONSES = [
    ("Data Center Expansion", EXAMPLE_RESPONSE_DATA_CENTER),
    ("Carbon Credit Program", EXAMPLE_RESPONSE_CARBON_CREDIT),
]
