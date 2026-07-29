"""Operations Agent example scenarios."""

from .schema import OperationsAgentRequest

SCENARIO_PRODUCT_LAUNCH = OperationsAgentRequest(
    scenario=(
        "We plan to launch a new product in 3 months. This requires coordination "
        "across engineering, design, QA, marketing, and sales enablement. "
        "Engineering estimates 8 weeks of development remaining."
    ),
    context="Current team: fully utilized on existing product. No slack capacity. Last launch took 5 months.",
)

SCENARIO_INTERNATIONAL_EXPANSION = OperationsAgentRequest(
    scenario=(
        "Expanding operations into EU markets requires local warehousing, "
        "multilingual support team, GDPR-compliant processes, and new "
        "vendor relationships for last-mile delivery."
    ),
    context="No international operations experience. Team of 85, all US-based. Target go-live: 6 months.",
)

SCENARIO_PROCESS_AUTOMATION = OperationsAgentRequest(
    scenario=(
        "Proposal to automate customer onboarding process end-to-end. Currently "
        "manual, taking 3 full-time team members. Automation would require "
        "integration with 4 systems and development of custom workflows."
    ),
    context="Current manual process handles 200 customers/month. Growth target: 500/month by year-end.",
)

SCENARIO_VENDOR_MIGRATION = OperationsAgentRequest(
    scenario=(
        "We need to migrate from our current cloud provider to a new one due to "
        "cost concerns. This affects all production systems, data pipelines, "
        "and 12 microservices."
    ),
    context="Current infrastructure: 12 services, 4TB data, 99.9% uptime SLA. Zero-downtime migration required.",
)

SCENARIO_OFFICE_CONSOLIDATION = OperationsAgentRequest(
    scenario=(
        "Consolidating three small offices into one larger headquarters. "
        "Requires physical move, IT infrastructure setup, and coordinating "
        "80 employees across different lease expiration dates."
    ),
    context="Lease expirations: Office A (2 months), Office B (5 months), Office C (8 months). New space available now.",
)

ALL_SCENARIOS = [
    ("Product Launch", SCENARIO_PRODUCT_LAUNCH),
    ("International Expansion", SCENARIO_INTERNATIONAL_EXPANSION),
    ("Process Automation", SCENARIO_PROCESS_AUTOMATION),
    ("Vendor Migration", SCENARIO_VENDOR_MIGRATION),
    ("Office Consolidation", SCENARIO_OFFICE_CONSOLIDATION),
]

ALL_EXAMPLE_RESPONSES = []
