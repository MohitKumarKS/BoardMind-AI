"""IT Agent example scenarios."""

from .schema import ITAgentRequest

SCENARIO_AI_PLATFORM = ITAgentRequest(
    scenario=(
        "We want to build an internal AI/ML platform that allows product teams to "
        "deploy machine learning models without DevOps support. This includes a model "
        "registry, automated training pipelines, and inference endpoints."
    ),
    context="Current stack: AWS, Kubernetes, Python services. No existing ML infrastructure. Team: 30 engineers, 0 ML engineers.",
)

SCENARIO_CLOUD_MIGRATION = ITAgentRequest(
    scenario=(
        "Proposal to migrate our entire production infrastructure from AWS to Google "
        "Cloud Platform to leverage their AI services and reduce costs by 20%."
    ),
    context="12 microservices, 4TB data, 99.9% uptime SLA. Last migration (on-prem to AWS) took 8 months and had 3 incidents.",
)

SCENARIO_REAL_TIME_ANALYTICS = ITAgentRequest(
    scenario=(
        "Marketing wants real-time customer behavior analytics that tracks user "
        "interactions across web, mobile, and email in a unified dashboard with "
        "sub-second query latency."
    ),
    context="Current analytics: batch processing with 24-hour delay. Data volume: 50M events/day growing 30% MoM.",
)

SCENARIO_ZERO_TRUST = ITAgentRequest(
    scenario=(
        "Security team recommends implementing zero-trust architecture across all "
        "internal systems. This includes identity verification for every request, "
        "micro-segmentation, and continuous authorization."
    ),
    context="Current: perimeter-based security with VPN. 200+ internal services. Remote workforce across 8 countries.",
)

SCENARIO_API_MARKETPLACE = ITAgentRequest(
    scenario=(
        "Product team wants to create a public API marketplace allowing third-party "
        "developers to build integrations with our platform. Includes developer portal, "
        "OAuth2 authentication, rate limiting, and usage-based billing."
    ),
    context="Current APIs: internal only, no versioning, inconsistent documentation. 15 core API endpoints.",
)

ALL_SCENARIOS = [
    ("AI/ML Platform", SCENARIO_AI_PLATFORM),
    ("Cloud Migration", SCENARIO_CLOUD_MIGRATION),
    ("Real-time Analytics", SCENARIO_REAL_TIME_ANALYTICS),
    ("Zero Trust Architecture", SCENARIO_ZERO_TRUST),
    ("API Marketplace", SCENARIO_API_MARKETPLACE),
]

ALL_EXAMPLE_RESPONSES = []
