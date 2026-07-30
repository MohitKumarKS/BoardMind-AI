"""Compliance Officer Agent example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Compliance Agent's output quality
2. Demonstrating the expected style of regulatory reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    ComplianceAgentRequest,
    ComplianceAgentResponse,
    ComplianceDomainAssessment,
    Position,
    ComplianceStatus,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_DATA_COLLECTION = ComplianceAgentRequest(
    scenario=(
        "Product team wants to implement behavioral tracking across our web "
        "application to feed our ML recommendation engine. This includes "
        "page views, click patterns, session duration, scroll depth, and "
        "feature usage. We serve customers in US, EU, and UK markets. "
        "Data would be stored for 24 months."
    ),
    context=(
        "Current privacy infrastructure: cookie consent banner (basic), "
        "privacy policy last updated 8 months ago. No DPIA on file for "
        "behavioral tracking. 40% of users are EU-based. We use Google "
        "Analytics and Mixpanel as processors. SOC2 Type II certified."
    ),
)

SCENARIO_AI_TRAINING = ComplianceAgentRequest(
    scenario=(
        "Our data science team proposes using customer support conversations "
        "to train an internal AI model for automated ticket routing and "
        "response suggestion. The training dataset would include 500K "
        "historical tickets spanning 3 years. Customers were not informed "
        "their conversations would be used for AI training."
    ),
    context=(
        "Customer base includes healthcare (HIPAA) and financial services "
        "(GLBA) clients. Support tickets may contain PHI, financial data, "
        "and personal information. Current privacy policy mentions data "
        "usage for 'service improvement' but does not specifically mention "
        "AI/ML training. EU customers represent 35% of ticket volume."
    ),
)

SCENARIO_VENDOR_ONBOARDING = ComplianceAgentRequest(
    scenario=(
        "Engineering wants to onboard a new SaaS vendor for customer success "
        "analytics. The vendor would receive customer usage data, account "
        "information, and engagement scores. They are a Series A startup "
        "based in Israel with data centers in AWS EU-West. They have "
        "ISO27001 but no SOC2 report yet."
    ),
    context=(
        "We have 200+ enterprise customers with strict vendor management "
        "requirements. Our MSA commits to notifying customers of new "
        "sub-processors. PCI-DSS scope does not include this data. "
        "Israel has EU adequacy decision for GDPR data transfers."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_DATA_COLLECTION = ComplianceAgentResponse(
    agent_id="compliance",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.80,
    domain_assessment=ComplianceDomainAssessment(
        regulatory_impact=(
            "Directly triggers GDPR Article 35 (DPIA required for systematic "
            "monitoring of data subjects), Article 6 (lawful basis — legitimate "
            "interest requires balancing test), Article 13/14 (transparency "
            "obligations). UK GDPR mirrors these requirements post-Brexit. "
            "CCPA/CPRA applies to California users — requires opt-out for "
            "'sale or sharing' of personal information. ePrivacy Directive "
            "requires consent for non-essential cookies/tracking."
        ),
        compliance_gaps=(
            "Critical gaps: (1) No DPIA for behavioral profiling — required "
            "under GDPR Article 35(3)(a) for systematic monitoring. (2) Cookie "
            "consent banner is 'basic' — likely non-compliant with CJEU Planet49 "
            "requirements (must be granular, specific, informed). (3) Privacy "
            "policy 8 months old — does not reflect new ML processing purpose. "
            "(4) No legitimate interest assessment documented. (5) 24-month "
            "retention exceeds what is justifiable without specific basis."
        ),
        remediation_effort=(
            "Estimated 10-14 weeks: DPIA with DPO sign-off (3-4 weeks), "
            "consent management platform upgrade (2-3 weeks implementation), "
            "privacy policy rewrite with legal review (2 weeks), legitimate "
            "interest assessment (1 week), data retention policy for behavioral "
            "data (1 week), processor DPA reviews for GA/Mixpanel (2-3 weeks). "
            "Budget: $40K-$60K (legal + CMP tooling + consulting)."
        ),
        audit_readiness=(
            "SOC2 Type II impact: privacy criteria (P1.0-P8.0) need updated "
            "evidence. If remediation completes before next audit cycle, no "
            "impact on certification. Risk of qualified finding if tracking "
            "goes live without DPIA documentation. Recommend building audit "
            "evidence concurrently with remediation."
        ),
        compliance_status=ComplianceStatus.REQUIRES_REVIEW,
    ),
    summary=(
        "Conditionally support behavioral tracking — the use case is lawful "
        "but requires 10-14 weeks of compliance remediation before any tracking "
        "can begin, particularly DPIA and consent mechanism upgrades."
    ),
    rationale=(
        "Behavioral tracking for ML recommendations is a legitimate business "
        "purpose, but the regulatory obligations are substantial given our 40% "
        "EU user base. GDPR Article 35 explicitly requires a Data Protection "
        "Impact Assessment before 'systematic monitoring of a publicly accessible "
        "area on a large scale' — which this qualifies as.\n\n"
        "The most pressing gap is our consent infrastructure. The CJEU's Planet49 "
        "ruling and subsequent DPA enforcement actions make clear that cookie "
        "consent must be granular, specific, and freely given. Our 'basic' banner "
        "almost certainly fails this standard. Without valid consent (or a "
        "documented legitimate interest with balancing test), all behavioral "
        "data collected from EU users would be unlawfully processed — creating "
        "exposure to GDPR fines of up to 4% of annual turnover.\n\n"
        "The path forward is clear: invest 10-14 weeks in compliance "
        "infrastructure before activating tracking. This is not optional — "
        "it is a legal requirement. The good news is that once built, this "
        "infrastructure supports all future data processing activities, "
        "making it a reusable investment rather than a one-time cost."
    ),
    risks=[
        "GDPR enforcement — processing without DPIA constitutes procedural violation subject to administrative fines up to €10M or 2% of global turnover",
        "Invalid consent — tracking EU users without GDPR-compliant consent creates immediate unlawful processing, with potential data deletion orders",
        "Cross-border transfer — Mixpanel US processing of EU behavioral data requires valid transfer mechanism (SCCs + TIA) post-Schrems II",
        "Class action exposure — GDPR Article 80 allows representative actions; behavioral tracking is a common target for privacy advocacy groups",
    ],
    conditions=[
        "Complete and publish DPIA before any behavioral tracking begins — no exceptions",
        "Upgrade consent management to granular, GDPR-compliant mechanism with documented valid consent",
        "Reduce retention period from 24 months to maximum justifiable period (recommend 12 months with review)",
        "Update privacy policy and provide Article 13 notice to all users before tracking activation",
    ],
    metrics_to_track=[
        "Consent rate — percentage of users providing valid consent for tracking (target >60% for viable dataset)",
        "DSAR volume — monitor for increase in data subject access/deletion requests post-implementation",
        "Regulatory inquiry count — track any DPA inquiries related to tracking activities",
        "Compliance gap closure — 100% of identified gaps resolved before production activation",
        "Audit readiness score — internal assessment against SOC2 privacy criteria, target 100%",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Behavioral Data Collection", SCENARIO_DATA_COLLECTION),
    ("AI Training on Customer Data", SCENARIO_AI_TRAINING),
    ("New Vendor Onboarding", SCENARIO_VENDOR_ONBOARDING),
]

ALL_EXAMPLE_RESPONSES = [
    ("Behavioral Data Collection", EXAMPLE_RESPONSE_DATA_COLLECTION),
]
