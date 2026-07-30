"""CISO Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the CISO Agent's output quality
2. Demonstrating the expected style of security reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    CISOAgentRequest,
    CISOAgentResponse,
    CISODomainAssessment,
    Position,
    SecurityRisk,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_CLOUD_MIGRATION = CISOAgentRequest(
    scenario=(
        "We are planning to migrate our core customer database from on-premise "
        "servers to AWS. The database contains 2M customer records including PII "
        "(names, emails, phone numbers, addresses) and payment tokens. The migration "
        "would take 3 months with a hybrid period where data exists in both locations."
    ),
    context=(
        "Current security: SOC2 Type II certified, ISO27001 compliant. "
        "Database encrypted at rest with AES-256. No breaches in 4 years. "
        "AWS target: RDS with encryption, VPC isolation, IAM controls."
    ),
)

SCENARIO_THIRD_PARTY_API = CISOAgentRequest(
    scenario=(
        "Engineering wants to integrate a third-party AI API (startup, Series B, "
        "18 months old) for customer sentiment analysis. Customer support "
        "conversations would be sent to their API for processing. They claim "
        "SOC2 Type I certification and GDPR compliance."
    ),
    context=(
        "Our customers include healthcare and financial services companies. "
        "Support conversations may contain PHI and financial information. "
        "The vendor's SOC2 Type I was issued 6 months ago. They process "
        "data in US-East and EU-West regions."
    ),
)

SCENARIO_REMOTE_ACCESS = CISOAgentRequest(
    scenario=(
        "The HR team proposes allowing employees to use personal devices (BYOD) "
        "for accessing company email and collaboration tools. Currently all access "
        "requires company-issued laptops with MDM. The proposal would cover 200 "
        "employees in non-engineering roles."
    ),
    context=(
        "Current controls: CrowdStrike EDR on all devices, Okta SSO with MFA, "
        "Zscaler for network security. Engineering has access to source code "
        "and production systems. Non-engineering accesses email, Slack, and "
        "Google Workspace only."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_CLOUD_MIGRATION = CISOAgentResponse(
    agent_id="ciso",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.75,
    domain_assessment=CISODomainAssessment(
        threat_exposure=(
            "Migration introduces 3 primary threat vectors: (1) data-in-transit "
            "exposure during the 3-month hybrid period, (2) misconfigured AWS "
            "security groups exposing RDS instances, (3) credential sprawl from "
            "managing two environments simultaneously. Attack surface increases "
            "approximately 40% during hybrid operation."
        ),
        data_protection_impact=(
            "2M records with PII and payment tokens require encryption at all "
            "layers during migration. Dual-location storage doubles the data "
            "protection surface area for 3 months. Risk of data residue on "
            "decommissioned on-prem hardware requires certified destruction."
        ),
        compliance_posture=(
            "SOC2 Type II scope must be extended to cover AWS environment before "
            "migration begins. ISO27001 transition audit required. AWS shared "
            "responsibility model means we own encryption key management, access "
            "control, and network security configuration."
        ),
        security_investment=(
            "Estimated $180K for migration security: $60K penetration testing "
            "(pre and post), $45K AWS security tooling (GuardDuty, SecurityHub, "
            "Macie), $40K encryption key management (KMS + HSM), $35K security "
            "monitoring integration. Ongoing: +$15K/month cloud security posture."
        ),
        security_risk=SecurityRisk.HIGH,
    ),
    summary=(
        "Conditionally support cloud migration — the target architecture is "
        "securable but the 3-month hybrid period creates elevated risk requiring "
        "specific controls before data movement begins."
    ),
    rationale=(
        "The target state (AWS RDS with encryption, VPC isolation, IAM) is "
        "objectively more secure than most on-premise deployments when properly "
        "configured. AWS's security infrastructure exceeds what most organizations "
        "can maintain internally. The concern is not the destination — it's the "
        "journey.\n\n"
        "The 3-month hybrid period is the highest-risk phase. During this time, "
        "data exists in two locations, doubling our protection surface area. "
        "Any misconfiguration in either environment creates exposure. The migration "
        "pipeline itself (data transfer mechanism) becomes a high-value target. "
        "I require encrypted transfer channels, integrity verification at each "
        "stage, and real-time monitoring of both environments.\n\n"
        "Post-migration, our security posture improves: AWS provides superior "
        "physical security, automated patching, and native encryption. However, "
        "the shared responsibility model means we must properly configure IAM "
        "policies, security groups, and monitoring. Misconfigurations are the "
        "#1 cause of cloud breaches."
    ),
    risks=[
        "Data exposure during hybrid period — dual-location increases breach surface area by approximately 40% for 3 months",
        "AWS misconfiguration — security groups, IAM policies, or S3 buckets incorrectly configured could expose 2M customer records",
        "Credential management complexity — operating two environments increases risk of credential leakage or over-privileged access",
        "Data residue on decommissioned on-premise hardware — requires certified data destruction (NIST 800-88)",
    ],
    conditions=[
        "Complete AWS security architecture review and approval before any data migration begins",
        "Implement encrypted migration pipeline with integrity verification checksums at each stage",
        "Extend SOC2 audit scope to include AWS environment prior to first data transfer",
        "Deploy cloud security posture management (CSPM) tooling before migration starts",
    ],
    metrics_to_track=[
        "AWS Security Hub score — maintain above 90% throughout migration",
        "Data transfer integrity — zero corruption or loss events during migration",
        "Unauthorized access attempts — alert on any anomalous access to migration pipeline",
        "Compliance gap count — target zero open findings before production cutover",
        "Mean time to detect misconfigurations — target <1 hour via automated scanning",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Cloud Migration", SCENARIO_CLOUD_MIGRATION),
    ("Third-Party API Integration", SCENARIO_THIRD_PARTY_API),
    ("BYOD Remote Access", SCENARIO_REMOTE_ACCESS),
]

ALL_EXAMPLE_RESPONSES = [
    ("Cloud Migration", EXAMPLE_RESPONSE_CLOUD_MIGRATION),
]
