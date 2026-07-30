"""Supply Chain Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Supply Chain Agent's output quality
2. Demonstrating the expected style of supply chain reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    SupplyChainAgentRequest,
    SupplyChainAgentResponse,
    SupplyChainDomainAssessment,
    Position,
    OperationalRisk,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_RESHORING = SupplyChainAgentRequest(
    scenario=(
        "We are considering reshoring our manufacturing from China to Mexico (nearshoring) "
        "to reduce lead times from 45 days to 12 days and mitigate geopolitical supply "
        "chain risk. The transition would affect 3 product lines representing 60% of revenue. "
        "Current China supplier has been reliable (98.5% on-time delivery) for 8 years."
    ),
    context=(
        "Annual procurement spend: $18M. China supplier cost advantage: 22% vs. Mexico options. "
        "Current inventory carrying costs: $2.4M/year (driven by long lead times). "
        "Tariff risk: potential 25% tariffs on China imports being discussed. "
        "Mexico supplier candidates: 3 qualified, 2 more in evaluation."
    ),
)

SCENARIO_NEW_DISTRIBUTION_CENTER = SupplyChainAgentRequest(
    scenario=(
        "Operations is proposing a new distribution center in the Southeast US to "
        "improve delivery times to our fastest-growing region. Currently all shipments "
        "originate from our single DC in Chicago. Southeast customers experience 4-5 day "
        "delivery vs. 1-2 days for Midwest customers."
    ),
    context=(
        "Southeast represents 30% of orders and growing 25% YoY. Current DC utilization: "
        "87% capacity. Average shipping cost to Southeast: $12.50/order vs. $6.80 Midwest. "
        "Customer complaints about delivery time: 40% from Southeast region. "
        "Estimated new DC cost: $3.5M buildout + $1.2M/year operations."
    ),
)

SCENARIO_SUPPLIER_CONSOLIDATION = SupplyChainAgentRequest(
    scenario=(
        "Procurement is recommending consolidating from 12 component suppliers down to 4 "
        "strategic partners to achieve volume discounts (estimated 15% cost reduction) and "
        "simplify vendor management. The top 4 suppliers currently handle 55% of volume "
        "and have the best quality and reliability scores."
    ),
    context=(
        "Current supplier performance: top 4 average 97% on-time, bottom 8 average 89% on-time. "
        "Quality defect rates: top 4 at 0.3%, bottom 8 at 1.8%. Annual procurement spend: $24M. "
        "Potential savings: $3.6M/year. Lead times range from 14 days (best) to 45 days (worst). "
        "Industry standard single-source risk threshold: no supplier >30% of total volume."
    ),
)

SCENARIO_DIRECT_TO_CONSUMER = SupplyChainAgentRequest(
    scenario=(
        "Sales is proposing launching a direct-to-consumer (DTC) channel alongside our "
        "existing B2B wholesale distribution. This requires individual order fulfillment "
        "capabilities (pick-pack-ship), returns processing, and last-mile delivery "
        "partnerships. Current operations are optimized for pallet-level B2B shipments."
    ),
    context=(
        "Current B2B order profile: 200 orders/day, average 50 units/order. "
        "Projected DTC volume: 500+ orders/day, average 1.5 units/order. "
        "B2B fulfillment cost: $2.50/unit. Estimated DTC fulfillment cost: $8-12/unit. "
        "Returns rate B2B: 2%. Expected DTC returns: 15-20%. "
        "Warehouse automation current: optimized for bulk, not individual picks."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_RESHORING = SupplyChainAgentResponse(
    agent_id="supply_chain",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.7,
    domain_assessment=SupplyChainDomainAssessment(
        supply_chain_impact=(
            "Lead time reduction from 45 to 12 days represents a 73% improvement, enabling "
            "shift from forecast-driven to demand-driven replenishment. Inventory carrying "
            "costs projected to decrease from $2.4M to $800K annually. However, 6-9 month "
            "transition period will require dual-sourcing with elevated inventory buffers."
        ),
        vendor_dependency=(
            "Current China supplier concentration (single source, 60% of revenue products) "
            "represents critical vendor dependency. Mexico transition diversifies geographic "
            "risk but creates new concentration if only 1-2 Mexico suppliers are qualified. "
            "Recommendation: qualify all 5 candidates before transition to maintain 3+ viable sources."
        ),
        logistics_complexity=(
            "Mexico nearshoring simplifies logistics significantly: ground freight vs. ocean, "
            "USMCA trade agreement benefits, same-timezone coordination. However, cross-border "
            "customs processes require new competency. Northern Mexico industrial corridors "
            "have mature logistics infrastructure supporting automotive and electronics."
        ),
        procurement_needs=(
            "Full supplier qualification for 3+ Mexico vendors: 90-120 day process including "
            "facility audits, pilot production (500-unit runs), quality certification, and "
            "capacity stress testing. Contract negotiation for volume commitments at target "
            "pricing must account for 22% cost gap — volume discounts and reduced logistics "
            "costs should close gap to 8-10%."
        ),
        operational_risk=OperationalRisk.HIGH,
    ),
    summary=(
        "Conditionally support nearshoring — strategic benefits are clear but transition "
        "execution must be sequenced to prevent supply disruption to 60% of revenue products."
    ),
    rationale=(
        "The strategic supply chain case for nearshoring is compelling. A 73% lead time "
        "reduction fundamentally changes our supply chain from push (forecast-driven, "
        "high inventory) to pull (demand-driven, lean inventory). The $1.6M annual savings "
        "in carrying costs alone partially offsets the procurement cost increase. Adding "
        "tariff risk mitigation makes the total cost picture increasingly favorable.\n\n"
        "However, the transition risk is significant because it affects 60% of revenue. "
        "Our China supplier has delivered 98.5% on-time over 8 years — that reliability "
        "level takes years to establish with new suppliers. The qualification process must "
        "not be rushed: pilot production runs, quality audits, and capacity stress tests "
        "are non-negotiable before shifting production volume.\n\n"
        "I recommend a 12-month phased transition: months 1-4 for full supplier qualification "
        "and pilot runs, months 5-8 for gradual volume shift (20% → 50% to Mexico), and "
        "months 9-12 for completing the transition while maintaining China as qualified "
        "backup supplier. Dual-sourcing during transition requires 60-day safety stock "
        "buffer, adding approximately $1.2M in temporary inventory investment."
    ),
    risks=[
        "New Mexico suppliers have unproven reliability at scale — 98.5% on-time performance takes years to validate",
        "Transition period dual-sourcing creates coordination complexity and elevated inventory costs ($1.2M temporary buffer)",
        "22% cost premium in Mexico erodes margins until volume discounts and logistics savings offset procurement increase",
        "Geopolitical risk is mitigated but not eliminated — USMCA trade agreement stability is assumed but not guaranteed",
    ],
    conditions=[
        "Complete qualification of minimum 3 Mexico suppliers before shifting any production volume from China",
        "Maintain China supplier relationship as qualified backup for 24 months post-transition (with minimum order commitments)",
        "Achieve 95%+ on-time delivery from Mexico suppliers in pilot runs before authorizing volume above 20%",
        "Build 60-day safety stock buffer ($1.2M inventory investment) before beginning transition to absorb variability",
    ],
    metrics_to_track=[
        "On-time delivery rate by supplier — Mexico suppliers must trend toward 97%+ within 6 months",
        "Lead time actual vs. target (12 days) — track weekly with root cause for deviations",
        "Inventory carrying cost — track reduction from $2.4M baseline toward $800K target",
        "Total landed cost per unit: Mexico vs. China — track gap closure toward 8-10% premium",
        "Supply disruption events — zero tolerance for stockouts on revenue-critical products during transition",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_CONSOLIDATION = SupplyChainAgentResponse(
    agent_id="supply_chain",
    round=1,
    position=Position.OPPOSE,
    confidence=0.68,
    domain_assessment=SupplyChainDomainAssessment(
        supply_chain_impact=(
            "Consolidation from 12 to 4 suppliers reduces management complexity but creates "
            "dangerous concentration. With 4 suppliers, each handles 25% of $24M volume ($6M). "
            "Loss of any single supplier disrupts 25% of supply — well above the industry "
            "standard 30% concentration threshold for critical components."
        ),
        vendor_dependency=(
            "Critical vendor concentration: 4 suppliers at 25% each means any single failure "
            "creates a major supply crisis. Current distributed model (12 suppliers) provides "
            "resilience — losing one supplier affects only 8% of volume. The 15% cost saving "
            "does not compensate for the tail-risk of a 25% supply disruption."
        ),
        logistics_complexity=(
            "Simplified logistics with fewer suppliers: reduced coordination overhead, "
            "standardized shipping schedules, and consolidated receiving. However, geographic "
            "concentration risk increases if selected 4 suppliers are in same region. "
            "Logistics simplification benefit is real but modest relative to risk introduced."
        ),
        procurement_needs=(
            "Volume consolidation to 4 suppliers enables significant negotiating leverage "
            "and estimated 15% cost reduction ($3.6M/year). However, requires renegotiating "
            "contracts for much larger volume commitments, which reduces future flexibility. "
            "Exit costs from 8 suppliers must also be considered (estimated $200-400K)."
        ),
        operational_risk=OperationalRisk.CRITICAL,
    ),
    summary=(
        "Oppose aggressive consolidation to 4 suppliers — concentration risk exceeds "
        "industry safety thresholds and a single supplier failure would be catastrophic."
    ),
    rationale=(
        "While the financial case for consolidation is attractive ($3.6M annual savings), "
        "the supply chain risk profile is unacceptable. Reducing to 4 suppliers means each "
        "handles 25% of our volume. If any single supplier experiences a disruption — fire, "
        "bankruptcy, quality issue, natural disaster — we lose a quarter of our supply with "
        "no immediate alternative. The industry standard maximum concentration for critical "
        "components is 30%, and we would be operating at the limit with zero margin.\n\n"
        "The performance data supports a more nuanced approach. The bottom 8 suppliers "
        "average 89% on-time vs. 97% for the top 4 — but this doesn't mean all 8 are poor. "
        "Likely 3-4 of the bottom 8 are genuinely underperforming and should be replaced, "
        "while others provide valuable diversification. I recommend identifying the true "
        "underperformers rather than applying a blanket consolidation.\n\n"
        "My counter-proposal: consolidate from 12 to 6-7 suppliers (eliminating only the "
        "genuinely underperforming vendors), with a maximum concentration of 20% per supplier. "
        "This captures approximately 60% of the cost savings ($2.2M) while maintaining "
        "supply chain resilience. The remaining suppliers provide qualified backup capacity "
        "that can be activated within 2-4 weeks if a primary supplier fails."
    ),
    risks=[
        "Single supplier failure at 25% concentration creates catastrophic supply gap — estimated 6-8 weeks to recover",
        "Volume dependence gives remaining suppliers excessive negotiating power at next contract renewal",
        "Geographic concentration: if selected suppliers cluster in one region, natural disaster or policy change affects all",
        "Quality issues at a concentrated supplier have 4x the impact vs. distributed model — recall risk amplified",
    ],
    conditions=[
        "Maximum concentration per supplier must not exceed 20% of total volume for any critical component",
        "Maintain minimum 6 qualified suppliers to ensure backup capacity for any disruption scenario",
        "Require geographic diversification: no two primary suppliers in same natural disaster risk zone",
        "Implement dual-source policy for all components representing >$1M annual spend",
    ],
    metrics_to_track=[
        "Supplier concentration ratio — Herfindahl index must remain below 0.15 (moderate concentration)",
        "Supply chain resilience score: time-to-recover from single supplier loss — target below 2 weeks",
        "Supplier financial health monitoring — quarterly assessment of all primary suppliers",
        "On-time delivery by supplier — track improvement trajectory post-consolidation",
        "Total cost of risk: savings achieved minus estimated risk exposure value (probability × impact)",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Nearshoring from China to Mexico", SCENARIO_RESHORING),
    ("New Distribution Center", SCENARIO_NEW_DISTRIBUTION_CENTER),
    ("Supplier Consolidation", SCENARIO_SUPPLIER_CONSOLIDATION),
    ("Direct-to-Consumer Channel", SCENARIO_DIRECT_TO_CONSUMER),
]

ALL_EXAMPLE_RESPONSES = [
    ("Nearshoring from China to Mexico", EXAMPLE_RESPONSE_RESHORING),
    ("Supplier Consolidation", EXAMPLE_RESPONSE_CONSOLIDATION),
]
