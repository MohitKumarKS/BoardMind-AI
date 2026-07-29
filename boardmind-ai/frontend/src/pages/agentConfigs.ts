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
