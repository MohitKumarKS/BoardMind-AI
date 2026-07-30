/**
 * Agent configurations for Department Workspace pages.
 * Each config defines the UI rendering for a specific department agent.
 */

import { AgentConfig } from "./AgentWorkspacePage";

export const marketingConfig: AgentConfig = {
  id: "marketing",
  title: "Marketing Agent",
  role: "CMO",
  subtitle:
    "Chief Marketing Officer perspective — brand strategy, market positioning, customer acquisition, and competitive advantage",
  color: "var(--color-marketing)",
  endpoint: "marketing",
  examples: [
    {
      label: "New Product Launch",
      scenario:
        "We are considering launching a new B2B SaaS product targeting mid-market companies. The product is an AI-powered analytics dashboard priced at $2,000/month. Our brand is currently known for enterprise solutions.",
    },
    {
      label: "Company Rebrand",
      scenario:
        "The leadership team is considering a full company rebrand including new name, visual identity, and messaging framework. The current brand has 8 years of equity but is perceived as 'legacy' by younger buyers.",
    },
    {
      label: "Market Expansion",
      scenario:
        "Our US-based platform is considering expansion into European markets starting with UK and Germany. We need localized marketing, local partnerships, and region-specific content strategy.",
    },
    {
      label: "Pricing Change",
      scenario:
        "The finance team proposes increasing prices by 25% for all new customers while grandfathering existing customers for 12 months. Current pricing is seen as 'affordable' in the market.",
    },
    {
      label: "Cloud Partnership",
      scenario:
        "A major cloud provider has offered a co-marketing partnership where they would feature our product in their marketplace and co-fund $500K in joint marketing campaigns over 12 months.",
    },
  ],
  domainFields: [
    { key: "market_opportunity", label: "Market Opportunity" },
    { key: "brand_impact", label: "Brand Impact" },
    { key: "competitive_position", label: "Competitive Position" },
    { key: "customer_segments_affected", label: "Customer Segments Affected" },
    { key: "go_to_market_complexity", label: "Go-to-Market Complexity" },
  ],
  extraListFields: [
    { key: "recommended_actions", label: "Recommended Actions", bulletColor: "var(--color-marketing)" },
  ],
};

export const salesConfig: AgentConfig = {
  id: "sales",
  title: "Sales Agent",
  role: "CRO",
  subtitle:
    "Chief Revenue Officer perspective — revenue growth, pipeline health, deal velocity, and customer relationships",
  color: "var(--color-sales)",
  endpoint: "sales",
  examples: [
    {
      label: "New Product Sales",
      scenario:
        "We're launching an AI analytics product at $2,000/month targeting mid-market. Sales team believes 50 customers achievable in Year 1. Need to build new sales playbook and potentially hire 2 account executives.",
    },
    {
      label: "Price Increase",
      scenario:
        "Finance proposes 25% price increase for new customers, grandfathering existing accounts for 12 months. Current ACV is $36K. Win rate is 32%. Top competitor is priced 20% higher.",
    },
    {
      label: "White-Label Partnership",
      scenario:
        "A Fortune 500 company wants to white-label our product for their customer base of 2,000 mid-market companies. They propose a 40% revenue share arrangement.",
    },
    {
      label: "Feature Delay",
      scenario:
        "Engineering says the enterprise SSO and audit logging features will be delayed 3 months. These features are in 8 active enterprise deals worth $1.2M total.",
    },
    {
      label: "Vertical Expansion",
      scenario:
        "Marketing wants us to expand into healthcare vertical. Requires HIPAA compliance features and industry-specific positioning. Estimated 6-month development timeline.",
    },
  ],
  domainFields: [
    { key: "revenue_upside", label: "Revenue Upside" },
    { key: "revenue_risk", label: "Revenue Risk" },
    { key: "pipeline_impact", label: "Pipeline Impact" },
    { key: "deal_cycle_effect", label: "Deal Cycle Effect" },
    { key: "competitive_effect", label: "Competitive Effect" },
  ],
  extraTextField: { key: "customer_impact", label: "Customer Impact" },
};

export const hrConfig: AgentConfig = {
  id: "hr",
  title: "HR Agent",
  role: "CHRO",
  subtitle:
    "Chief Human Resources Officer perspective — people impact, organizational health, talent strategy, and culture",
  color: "var(--color-hr)",
  endpoint: "hr",
  examples: [
    {
      label: "Mass Hiring",
      scenario:
        "Engineering requests 8 additional software engineers to accelerate development. Current team is 12. This would represent 67% headcount growth in one department within a 3-month hiring window.",
    },
    {
      label: "Remote to Office",
      scenario:
        "Leadership wants to mandate 4 days/week in-office starting next quarter. Currently the policy is 2 days/week. 40% of the team was hired as remote-first during 2021-2022.",
    },
    {
      label: "Restructure",
      scenario:
        "We are merging the Product and Engineering departments into a single 'Product & Technology' organization. This eliminates the VP Product role and creates a new CTO/CPO hybrid position.",
    },
    {
      label: "Stack Ranking",
      scenario:
        "Finance proposes implementing a stack-ranking performance system to identify bottom 10% performers for performance improvement plans. Goal is to 'raise the bar' on talent quality.",
    },
    {
      label: "Offshore Team",
      scenario:
        "Operations proposes establishing a 20-person offshore development team in India to reduce engineering costs by 40%. Onshore team would focus on architecture while offshore handles implementation.",
    },
  ],
  domainFields: [
    { key: "headcount_change", label: "Headcount Change" },
    { key: "skill_gap", label: "Skill Gap" },
    { key: "culture_impact", label: "Culture Impact" },
    { key: "change_complexity", label: "Change Complexity" },
    { key: "timeline_to_readiness", label: "Timeline to Readiness" },
  ],
  extraListFields: [
    { key: "change_management_needs", label: "Change Management Needs", bulletColor: "var(--color-hr)" },
  ],
};

export const operationsConfig: AgentConfig = {
  id: "operations",
  title: "Operations Agent",
  role: "COO",
  subtitle:
    "Chief Operating Officer perspective — execution feasibility, process efficiency, delivery reliability, and scalability",
  color: "var(--color-operations)",
  endpoint: "operations",
  examples: [
    {
      label: "Product Launch",
      scenario:
        "We plan to launch a new product in 3 months. This requires coordination across engineering, design, QA, marketing, and sales enablement. Engineering estimates 8 weeks of development remaining.",
    },
    {
      label: "International Expansion",
      scenario:
        "Expanding operations into EU markets requires local warehousing, multilingual support team, GDPR-compliant processes, and new vendor relationships for last-mile delivery.",
    },
    {
      label: "Process Automation",
      scenario:
        "Proposal to automate customer onboarding process end-to-end. Currently manual, taking 3 full-time team members. Automation would require integration with 4 systems.",
    },
    {
      label: "Vendor Migration",
      scenario:
        "We need to migrate from our current cloud provider to a new one due to cost concerns. This affects all production systems, data pipelines, and 12 microservices.",
    },
    {
      label: "Office Consolidation",
      scenario:
        "Consolidating three small offices into one larger headquarters. Requires physical move, IT infrastructure setup, and coordinating 80 employees across different lease expiration dates.",
    },
  ],
  domainFields: [
    { key: "execution_complexity", label: "Execution Complexity" },
    { key: "timeline_estimate", label: "Timeline Estimate" },
    { key: "resource_requirements", label: "Resource Requirements" },
    { key: "capacity_impact", label: "Capacity Impact" },
    { key: "dependencies", label: "Dependencies" },
  ],
  extraListFields: [
    { key: "implementation_phases", label: "Implementation Phases", bulletColor: "var(--color-operations)" },
  ],
};

export const legalConfig: AgentConfig = {
  id: "legal",
  title: "Legal Agent",
  role: "GC",
  subtitle:
    "General Counsel perspective — regulatory compliance, liability exposure, contracts, IP, and data privacy",
  color: "var(--color-legal)",
  endpoint: "legal",
  examples: [
    {
      label: "Data Product",
      scenario:
        "We want to launch a product that collects user behavioral data to provide personalized recommendations. Data would be stored in US-based servers but we plan to serve customers in EU and California.",
    },
    {
      label: "Startup Acquisition",
      scenario:
        "We are considering acquiring a 15-person startup for their AI technology. They have 2 patents pending and several open-source dependencies in their core product. Purchase price: $4M.",
    },
    {
      label: "Competitor Partnership",
      scenario:
        "A competitor proposes a joint venture to co-develop a new product category. They would contribute distribution, we contribute technology. Revenue split: 60/40.",
    },
    {
      label: "Employee Monitoring",
      scenario:
        "HR wants to implement AI-based performance monitoring that tracks employee productivity metrics including screen time, communication frequency, and project completion velocity.",
    },
    {
      label: "Open Source Strategy",
      scenario:
        "Engineering proposes open-sourcing our core analytics library under MIT license to build community and attract developer talent. The library contains algorithms that are key differentiators.",
    },
  ],
  domainFields: [
    { key: "compliance_status", label: "Compliance Status" },
    { key: "risk_level", label: "Risk Level" },
    { key: "liability_exposure", label: "Liability Exposure" },
    { key: "regulatory_bodies", label: "Regulatory Bodies" },
    { key: "ip_implications", label: "IP Implications" },
  ],
  extraListFields: [
    { key: "required_safeguards", label: "Required Safeguards", bulletColor: "var(--color-legal)" },
  ],
};

export const itConfig: AgentConfig = {
  id: "it",
  title: "IT Agent",
  role: "CTO",
  subtitle:
    "Chief Technology Officer perspective — technical feasibility, cybersecurity, infrastructure, and system architecture",
  color: "var(--color-it)",
  endpoint: "it",
  examples: [
    {
      label: "AI/ML Platform",
      scenario:
        "We want to build an internal AI/ML platform that allows product teams to deploy machine learning models without DevOps support. This includes a model registry, automated training pipelines, and inference endpoints.",
    },
    {
      label: "Cloud Migration",
      scenario:
        "Proposal to migrate our entire production infrastructure from AWS to Google Cloud Platform to leverage their AI services and reduce costs by 20%.",
    },
    {
      label: "Real-time Analytics",
      scenario:
        "Marketing wants real-time customer behavior analytics that tracks user interactions across web, mobile, and email in a unified dashboard with sub-second query latency.",
    },
    {
      label: "Zero Trust",
      scenario:
        "Security team recommends implementing zero-trust architecture across all internal systems including identity verification for every request, micro-segmentation, and continuous authorization.",
    },
    {
      label: "API Marketplace",
      scenario:
        "Product team wants to create a public API marketplace allowing third-party developers to build integrations with our platform. Includes developer portal, OAuth2, rate limiting, and usage-based billing.",
    },
  ],
  domainFields: [
    { key: "feasibility", label: "Feasibility" },
    { key: "security_risk", label: "Security Risk" },
    { key: "infrastructure_needs", label: "Infrastructure Needs" },
    { key: "integration_complexity", label: "Integration Complexity" },
    { key: "technical_debt_impact", label: "Technical Debt Impact" },
  ],
  extraTextField: { key: "effort_estimate", label: "Effort Estimate" },
};

export const analyticsConfig: AgentConfig = {
  id: "business_analytics",
  title: "Business Analytics Agent",
  role: "CDO",
  subtitle:
    "Chief Data Officer perspective — data-driven evidence, measurement rigor, statistical validity, and analytical objectivity",
  color: "var(--color-analytics)",
  endpoint: "business_analytics",
  examples: [
    {
      label: "Conversion Claims",
      scenario:
        "Product team claims that redesigning the onboarding flow will increase trial-to-paid conversion by 25%. They base this on qualitative user feedback and one competitor's published case study.",
    },
    {
      label: "Market Size Validation",
      scenario:
        "Marketing estimates our Total Addressable Market at $5B based on a third-party analyst report. They propose a $2M investment to capture 1% market share within 18 months.",
    },
    {
      label: "Churn Prediction",
      scenario:
        "Customer Success wants to build a churn prediction model using historical data to proactively intervene with at-risk accounts. They project 30% churn reduction within 6 months.",
    },
    {
      label: "Pricing Experiment",
      scenario:
        "Revenue team proposes A/B testing three new pricing tiers to optimize ARPU. Test would run for 6 weeks on 20% of new signups. Expected uplift: 15-25% ARPU.",
    },
    {
      label: "Productivity Claims",
      scenario:
        "Management claims the new AI copilot tool increased developer productivity by 40%. They want to expand it company-wide based on a 2-week pilot with 8 volunteer developers.",
    },
  ],
  domainFields: [
    { key: "evidence_strength", label: "Evidence Strength" },
    { key: "data_availability", label: "Data Availability" },
    { key: "projection_confidence", label: "Projection Confidence" },
    { key: "key_metrics", label: "Key Metrics" },
    { key: "benchmarks", label: "Benchmarks" },
  ],
  extraTextField: { key: "measurement_plan", label: "Measurement Plan" },
};

// --- New 12 Executive Agents ---

export const ceoConfig: AgentConfig = {
  id: "ceo",
  title: "CEO Agent",
  role: "CEO",
  subtitle: "Chief Executive Officer perspective — strategic vision, corporate direction, stakeholder alignment, and executive prioritization",
  color: "var(--color-ceo)",
  endpoint: "analyze/ceo",
  examples: [
    { label: "Strategic Pivot", scenario: "The board is considering pivoting our core business from on-premise software to a cloud-native SaaS model. This would require $15M in investment over 2 years and potentially disrupt relationships with our 200 enterprise customers." },
    { label: "Acquisition", scenario: "A competitor with complementary technology and 50 enterprise clients is available for acquisition at $25M. This would double our market share but require significant integration effort." },
    { label: "International Expansion", scenario: "We have an opportunity to expand into the APAC market through a joint venture with a local technology firm. The partner brings distribution but we would share IP." },
  ],
  domainFields: [
    { key: "strategic_alignment", label: "Strategic Alignment" },
    { key: "stakeholder_impact", label: "Stakeholder Impact" },
    { key: "competitive_positioning", label: "Competitive Positioning" },
    { key: "execution_priority", label: "Execution Priority" },
    { key: "risk_level", label: "Risk Level" },
  ],
  extraListFields: [
    { key: "conditions", label: "Conditions for Support", bulletColor: "var(--color-ceo)" },
  ],
};

export const cisoConfig: AgentConfig = {
  id: "ciso",
  title: "CISO Agent",
  role: "CISO",
  subtitle: "Chief Information Security Officer perspective — cybersecurity, threat assessment, data protection, and security compliance",
  color: "var(--color-ciso)",
  endpoint: "analyze/ciso",
  examples: [
    { label: "Cloud Migration", scenario: "We are migrating our entire production infrastructure from on-premise data centers to AWS. This includes customer PII data, financial records, and proprietary algorithms." },
    { label: "Third-Party API", scenario: "The product team wants to integrate with a third-party AI service that requires sending customer data to external servers for processing. The vendor is SOC2 Type II certified." },
    { label: "Remote Workforce", scenario: "We are implementing a permanent hybrid work model allowing employees to use personal devices for accessing company systems including source code and customer databases." },
  ],
  domainFields: [
    { key: "threat_exposure", label: "Threat Exposure" },
    { key: "data_protection_impact", label: "Data Protection Impact" },
    { key: "compliance_posture", label: "Security Compliance" },
    { key: "security_investment", label: "Security Investment" },
    { key: "security_risk", label: "Security Risk Level" },
  ],
  extraListFields: [
    { key: "conditions", label: "Security Requirements", bulletColor: "var(--color-ciso)" },
  ],
};

export const riskConfig: AgentConfig = {
  id: "risk",
  title: "Risk Agent",
  role: "CRO-Risk",
  subtitle: "Chief Risk Officer perspective — enterprise risk management, risk quantification, and scenario analysis",
  color: "var(--color-risk)",
  endpoint: "analyze/risk",
  examples: [
    { label: "Market Entry", scenario: "We are entering the healthcare market which requires HIPAA compliance and carries significant regulatory risk. Failure could result in fines up to $1.5M per incident." },
    { label: "Vendor Concentration", scenario: "80% of our revenue depends on a single cloud provider's marketplace. They recently changed their commission structure and could delist us at any time." },
    { label: "Aggressive Growth", scenario: "The board wants to 3x revenue in 18 months by simultaneously launching 4 new products, expanding to 3 new markets, and doubling headcount." },
  ],
  domainFields: [
    { key: "risk_exposure", label: "Risk Exposure" },
    { key: "probability_assessment", label: "Probability Assessment" },
    { key: "mitigation_strategy", label: "Mitigation Strategy" },
    { key: "residual_risk", label: "Residual Risk" },
    { key: "risk_level", label: "Risk Level" },
  ],
  extraListFields: [
    { key: "conditions", label: "Risk Conditions", bulletColor: "var(--color-risk)" },
  ],
};

export const complianceConfig: AgentConfig = {
  id: "compliance",
  title: "Compliance Agent",
  role: "CCO",
  subtitle: "Chief Compliance Officer perspective — regulatory compliance, governance frameworks, and audit readiness",
  color: "var(--color-compliance)",
  endpoint: "analyze/compliance",
  examples: [
    { label: "Behavioral Tracking", scenario: "Product wants to implement user behavioral tracking across our platform to improve recommendations. This involves collecting browsing patterns, click data, and session recordings from EU and US users." },
    { label: "AI Training Data", scenario: "The ML team wants to use customer data to train our AI models. Customers signed terms that mention 'service improvement' but don't explicitly mention AI training." },
    { label: "Vendor Onboarding", scenario: "We are onboarding a new payment processor based in India that will handle European customer transactions. They claim PCI-DSS Level 1 certification." },
  ],
  domainFields: [
    { key: "regulatory_impact", label: "Regulatory Impact" },
    { key: "compliance_gaps", label: "Compliance Gaps" },
    { key: "remediation_effort", label: "Remediation Effort" },
    { key: "audit_readiness", label: "Audit Readiness" },
    { key: "compliance_status", label: "Compliance Status" },
  ],
  extraListFields: [
    { key: "conditions", label: "Compliance Conditions", bulletColor: "var(--color-compliance)" },
  ],
};

export const strategyConfig: AgentConfig = {
  id: "strategy",
  title: "Strategy Agent",
  role: "CSO",
  subtitle: "Chief Strategy Officer perspective — competitive analysis, market positioning, and long-term strategic planning",
  color: "var(--color-strategy)",
  endpoint: "analyze/strategy",
  examples: [
    { label: "Market Disruption", scenario: "A well-funded startup just launched a product at 60% of our price with 80% of our features. They raised $50M and are targeting our mid-market segment." },
    { label: "Platform Strategy", scenario: "We are considering transforming from a standalone product into a platform by opening APIs and building an ecosystem of third-party integrations." },
    { label: "Vertical Focus", scenario: "Should we narrow our focus from serving all industries to becoming the dominant solution in 3 specific verticals (healthcare, fintech, education)?" },
  ],
  domainFields: [
    { key: "market_opportunity", label: "Market Opportunity" },
    { key: "competitive_advantage", label: "Competitive Advantage" },
    { key: "strategic_fit", label: "Strategic Fit" },
    { key: "execution_complexity", label: "Execution Complexity" },
    { key: "strategic_priority", label: "Strategic Priority" },
  ],
  extraListFields: [
    { key: "conditions", label: "Strategic Conditions", bulletColor: "var(--color-strategy)" },
  ],
};

export const productConfig: AgentConfig = {
  id: "product",
  title: "Product Agent",
  role: "CPO",
  subtitle: "Chief Product Officer perspective — product strategy, roadmap prioritization, product-market fit, and user experience",
  color: "var(--color-product)",
  endpoint: "analyze/product",
  examples: [
    { label: "Feature Request", scenario: "Enterprise customers are requesting white-label capabilities which would require 4 months of engineering effort and change our product architecture significantly." },
    { label: "Build vs Buy", scenario: "We need real-time analytics. Should we build it in-house (6 months, $800K) or integrate with a third-party vendor ($200K/year, 2-week integration)?" },
    { label: "Platform Simplification", scenario: "Our product has 47 features but analytics show only 12 are used by more than 10% of users. Should we sunset the unused features to reduce complexity?" },
  ],
  domainFields: [
    { key: "product_market_fit", label: "Product-Market Fit" },
    { key: "roadmap_impact", label: "Roadmap Impact" },
    { key: "user_experience", label: "User Experience" },
    { key: "build_vs_buy", label: "Build vs Buy" },
    { key: "feasibility", label: "Feasibility" },
  ],
  extraListFields: [
    { key: "conditions", label: "Product Conditions", bulletColor: "var(--color-product)" },
  ],
};

export const customerSuccessConfig: AgentConfig = {
  id: "customer_success",
  title: "Customer Success Agent",
  role: "CCusO",
  subtitle: "Chief Customer Officer perspective — customer retention, satisfaction, NPS/CSAT, and lifecycle management",
  color: "var(--color-customer-success)",
  endpoint: "analyze/customer_success",
  examples: [
    { label: "Price Increase", scenario: "Finance wants to raise prices by 30% for all customers. Current NPS is 42 and annual churn is 8%. Our top 20 accounts represent 60% of revenue." },
    { label: "Feature Removal", scenario: "Engineering wants to deprecate a legacy feature used by 15% of customers to reduce maintenance burden. These customers are mostly on our lowest tier." },
    { label: "Support Model Change", scenario: "We are moving from dedicated account managers to a pooled support model with AI-first triage. Currently 85% customer satisfaction with dedicated model." },
  ],
  domainFields: [
    { key: "customer_impact", label: "Customer Impact" },
    { key: "retention_risk", label: "Retention Risk" },
    { key: "satisfaction_forecast", label: "Satisfaction Forecast" },
    { key: "support_requirements", label: "Support Requirements" },
    { key: "customer_risk", label: "Customer Risk" },
  ],
  extraListFields: [
    { key: "conditions", label: "Customer Conditions", bulletColor: "var(--color-customer-success)" },
  ],
};

export const supplyChainConfig: AgentConfig = {
  id: "supply_chain",
  title: "Supply Chain Agent",
  role: "CSCO",
  subtitle: "Chief Supply Chain Officer perspective — procurement, logistics, vendor management, and fulfillment",
  color: "var(--color-supply-chain)",
  endpoint: "analyze/supply_chain",
  examples: [
    { label: "Supplier Diversification", scenario: "Our primary component supplier in China provides 90% of our critical parts. Recent tariff changes and shipping delays have increased costs by 25%." },
    { label: "Warehouse Expansion", scenario: "We need to add West Coast fulfillment capability. Options are building our own facility ($5M) or partnering with a 3PL provider ($200K/month)." },
    { label: "Nearshoring", scenario: "We are evaluating moving manufacturing from Southeast Asia to Mexico to reduce lead times from 8 weeks to 2 weeks, at a 15% cost increase." },
  ],
  domainFields: [
    { key: "supply_chain_impact", label: "Supply Chain Impact" },
    { key: "vendor_dependency", label: "Vendor Dependency" },
    { key: "logistics_complexity", label: "Logistics Complexity" },
    { key: "procurement_needs", label: "Procurement Needs" },
    { key: "operational_risk", label: "Operational Risk" },
  ],
  extraListFields: [
    { key: "conditions", label: "Supply Chain Conditions", bulletColor: "var(--color-supply-chain)" },
  ],
};

export const esgConfig: AgentConfig = {
  id: "esg",
  title: "ESG Agent",
  role: "ESG",
  subtitle: "ESG & Sustainability Officer perspective — environmental impact, social responsibility, and governance standards",
  color: "var(--color-esg)",
  endpoint: "analyze/esg",
  examples: [
    { label: "Data Center Expansion", scenario: "We need to triple our compute capacity. Options are expanding existing data centers (fossil fuel grid) or building new ones in regions with renewable energy at 20% higher cost." },
    { label: "Supply Chain Audit", scenario: "An NGO report flagged potential labor violations in our tier-2 suppliers' factories. We currently have no visibility below tier-1 suppliers." },
    { label: "Carbon Commitment", scenario: "The board wants to commit to net-zero by 2030. Our current carbon footprint is 50,000 tonnes CO2e annually, primarily from cloud infrastructure and business travel." },
  ],
  domainFields: [
    { key: "environmental_impact", label: "Environmental Impact" },
    { key: "social_impact", label: "Social Impact" },
    { key: "governance_implications", label: "Governance Implications" },
    { key: "sustainability_score", label: "Sustainability Score" },
    { key: "esg_risk", label: "ESG Risk" },
  ],
  extraListFields: [
    { key: "conditions", label: "ESG Conditions", bulletColor: "var(--color-esg)" },
  ],
};

export const aiGovernanceConfig: AgentConfig = {
  id: "ai_governance",
  title: "AI Governance Agent",
  role: "AIGO",
  subtitle: "AI Governance & Ethics Officer perspective — AI ethics, algorithmic fairness, responsible AI, and model governance",
  color: "var(--color-ai-governance)",
  endpoint: "analyze/ai_governance",
  examples: [
    { label: "Hiring Algorithm", scenario: "HR wants to deploy an AI system that screens resumes and ranks candidates. The model was trained on 5 years of historical hiring data from our company." },
    { label: "Customer Scoring", scenario: "We want to implement AI-based credit scoring for our lending product using alternative data sources including social media activity and purchasing patterns." },
    { label: "Autonomous Decisions", scenario: "The product team proposes letting our AI system automatically approve or deny customer requests up to $10K without human review to reduce response time." },
  ],
  domainFields: [
    { key: "ethical_risk", label: "Ethical Risk" },
    { key: "transparency_requirements", label: "Transparency Requirements" },
    { key: "governance_framework", label: "Governance Framework" },
    { key: "societal_impact", label: "Societal Impact" },
    { key: "ai_risk_level", label: "AI Risk Level" },
  ],
  extraListFields: [
    { key: "conditions", label: "AI Governance Conditions", bulletColor: "var(--color-ai-governance)" },
  ],
};

export const innovationConfig: AgentConfig = {
  id: "innovation",
  title: "Innovation Agent",
  role: "CIO-Inn",
  subtitle: "Chief Innovation Officer perspective — R&D strategy, emerging technology, innovation pipeline, and patents",
  color: "var(--color-innovation)",
  endpoint: "analyze/innovation",
  examples: [
    { label: "Quantum Computing", scenario: "Should we invest $2M in a quantum computing research team to prepare for post-quantum cryptography requirements and explore quantum ML applications?" },
    { label: "Open Source Strategy", scenario: "Engineering proposes open-sourcing our core framework to build community and attract talent. The framework contains 3 patentable algorithms." },
    { label: "Innovation Lab", scenario: "We want to create a dedicated innovation lab with 10% of engineering capacity focused on moonshot projects with 3-5 year horizons and no immediate revenue expectation." },
  ],
  domainFields: [
    { key: "innovation_potential", label: "Innovation Potential" },
    { key: "technology_readiness", label: "Technology Readiness" },
    { key: "research_requirements", label: "Research Requirements" },
    { key: "ip_opportunity", label: "IP Opportunity" },
    { key: "innovation_risk", label: "Innovation Risk" },
  ],
  extraListFields: [
    { key: "conditions", label: "Innovation Conditions", bulletColor: "var(--color-innovation)" },
  ],
};

export const investorRelationsConfig: AgentConfig = {
  id: "investor_relations",
  title: "Investor Relations Agent",
  role: "IRO",
  subtitle: "Investor Relations Officer perspective — shareholder communication, market perception, and earnings impact",
  color: "var(--color-investor-relations)",
  endpoint: "analyze/investor_relations",
  examples: [
    { label: "Revenue Miss", scenario: "We are going to miss our quarterly revenue guidance by 12%. We need to prepare investor communications and decide whether to pre-announce or wait for earnings." },
    { label: "Acquisition Announcement", scenario: "We are acquiring a company for $50M (40% premium). We need to communicate this to shareholders and explain the strategic rationale and expected dilution." },
    { label: "Share Buyback", scenario: "We have $100M in cash reserves. The board is debating between a $30M share buyback program, a special dividend, or retaining cash for M&A opportunities." },
  ],
  domainFields: [
    { key: "market_perception", label: "Market Perception" },
    { key: "earnings_impact", label: "Earnings Impact" },
    { key: "shareholder_value", label: "Shareholder Value" },
    { key: "communication_strategy", label: "Communication Strategy" },
    { key: "investor_sentiment", label: "Investor Sentiment" },
  ],
  extraListFields: [
    { key: "conditions", label: "IR Conditions", bulletColor: "var(--color-investor-relations)" },
  ],
};
