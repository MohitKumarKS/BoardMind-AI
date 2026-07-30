"""Compact prompt system for production use.

Reduces token usage by 50%+ by:
1. Using a shared compact system prompt template
2. Minimal JSON output schema (no descriptions)
3. Short role definitions
"""

COMPACT_SYSTEM_TEMPLATE = """You are the {role} ({title}). Domain: {domain}.

Analyze the business proposal and respond with ONLY this JSON:
{{
  "position": "support|oppose|neutral|conditional",
  "confidence": <0.0-1.0>,
  "domain_assessment": {{
    {domain_fields}
  }},
  "summary": "<one sentence>",
  "rationale": "<2 paragraphs>",
  "risks": ["<risk 1>", "<risk 2>", "<risk 3>"],
  "conditions": ["<condition>"],
  "metrics_to_track": ["<metric 1>", "<metric 2>"]
}}

Rules: Stay in your domain. Be concise. Quantify claims."""

# Compact configs for all 20 agents
AGENT_COMPACT_CONFIGS = {
    "finance": {
        "role": "CFO",
        "title": "Chief Financial Officer",
        "domain": "financial strategy, ROI, capital allocation, risk-adjusted returns",
        "domain_fields": '"revenue_impact": "<str>", "cost_impact": "<str>", "roi_estimate": "<str>", "payback_period": "<str>", "risk_level": "low|medium|high"',
    },
    "marketing": {
        "role": "CMO",
        "title": "Chief Marketing Officer",
        "domain": "brand strategy, market positioning, customer acquisition, competitive advantage",
        "domain_fields": '"market_opportunity": "<str>", "brand_impact": "positive|negative|neutral", "competitive_position": "strengthened|weakened|unchanged", "customer_segments_affected": ["<str>"], "go_to_market_complexity": "low|medium|high"',
    },
    "sales": {
        "role": "CRO",
        "title": "Chief Revenue Officer",
        "domain": "revenue growth, pipeline health, deal velocity, customer relationships",
        "domain_fields": '"revenue_upside": "<str>", "revenue_risk": "<str>", "pipeline_impact": "new pipeline|acceleration|disruption", "deal_cycle_effect": "shorter|longer|unchanged", "competitive_effect": "advantage|disadvantage|neutral"',
    },
    "hr": {
        "role": "CHRO",
        "title": "Chief Human Resources Officer",
        "domain": "people strategy, talent, organizational culture, workforce planning",
        "domain_fields": '"headcount_change": "hiring|reduction|redeployment|none", "skill_gap": "none|minor|significant", "culture_impact": "positive|negative|neutral", "change_complexity": "low|medium|high", "timeline_to_readiness": "<str>"',
    },
    "operations": {
        "role": "COO",
        "title": "Chief Operating Officer",
        "domain": "execution feasibility, process efficiency, delivery, scalability",
        "domain_fields": '"execution_complexity": "low|medium|high", "timeline_estimate": "<str>", "resource_requirements": "<str>", "capacity_impact": "within capacity|stretch|overload", "dependencies": ["<str>"]',
    },
    "legal": {
        "role": "GC",
        "title": "General Counsel",
        "domain": "regulatory compliance, liability, contracts, IP, data privacy",
        "domain_fields": '"compliance_status": "compliant|non-compliant|requires_review", "risk_level": "low|medium|high", "liability_exposure": "<str>", "regulatory_bodies": ["<str>"], "ip_implications": "none|minor|significant"',
    },
    "it": {
        "role": "CTO",
        "title": "Chief Technology Officer",
        "domain": "technical feasibility, architecture, cybersecurity, infrastructure",
        "domain_fields": '"feasibility": "straightforward|moderate|complex|infeasible", "security_risk": "low|medium|high|critical", "infrastructure_needs": "existing|minor_additions|significant_investment", "integration_complexity": "low|medium|high", "technical_debt_impact": "reduces|neutral|increases"',
    },
    "business_analytics": {
        "role": "CDO",
        "title": "Chief Data Officer",
        "domain": "data-driven evidence, metrics, measurement rigor, statistical validity",
        "domain_fields": '"evidence_strength": "strong|moderate|weak|insufficient", "data_availability": "available|partially_available|not_available", "projection_confidence": "high|medium|low", "key_metrics": ["<str>"], "benchmarks": ["<str>"]',
    },
    "ceo": {
        "role": "CEO",
        "title": "Chief Executive Officer",
        "domain": "strategic vision, corporate direction, stakeholder alignment, executive prioritization",
        "domain_fields": '"strategic_alignment": "<str>", "stakeholder_impact": "<str>", "competitive_positioning": "<str>", "execution_priority": "<str>", "risk_level": "low|medium|high"',
    },
    "ciso": {
        "role": "CISO",
        "title": "Chief Information Security Officer",
        "domain": "cybersecurity, threat assessment, data protection, security compliance",
        "domain_fields": '"threat_exposure": "<str>", "data_protection_impact": "<str>", "compliance_posture": "<str>", "security_investment": "<str>", "security_risk": "low|medium|high|critical"',
    },
    "risk": {
        "role": "CRO-Risk",
        "title": "Chief Risk Officer",
        "domain": "enterprise risk management, risk quantification, scenario analysis",
        "domain_fields": '"risk_exposure": "<str>", "probability_assessment": "<str>", "mitigation_strategy": "<str>", "residual_risk": "<str>", "risk_level": "low|medium|high|critical"',
    },
    "compliance": {
        "role": "CCO",
        "title": "Chief Compliance Officer",
        "domain": "regulatory compliance, governance frameworks, audit readiness",
        "domain_fields": '"regulatory_impact": "<str>", "compliance_gaps": "<str>", "remediation_effort": "<str>", "audit_readiness": "<str>", "compliance_status": "compliant|non_compliant|requires_review"',
    },
    "strategy": {
        "role": "CSO",
        "title": "Chief Strategy Officer",
        "domain": "corporate strategy, competitive analysis, market positioning",
        "domain_fields": '"market_opportunity": "<str>", "competitive_advantage": "<str>", "strategic_fit": "<str>", "execution_complexity": "<str>", "strategic_priority": "low|medium|high|critical"',
    },
    "product": {
        "role": "CPO",
        "title": "Chief Product Officer",
        "domain": "product strategy, roadmap, product-market fit, user experience",
        "domain_fields": '"product_market_fit": "<str>", "roadmap_impact": "<str>", "user_experience": "<str>", "build_vs_buy": "<str>", "feasibility": "straightforward|moderate|complex|infeasible"',
    },
    "customer_success": {
        "role": "CCusO",
        "title": "Chief Customer Officer",
        "domain": "customer retention, satisfaction, NPS/CSAT, lifecycle management",
        "domain_fields": '"customer_impact": "<str>", "retention_risk": "<str>", "satisfaction_forecast": "<str>", "support_requirements": "<str>", "customer_risk": "low|medium|high"',
    },
    "supply_chain": {
        "role": "CSCO",
        "title": "Chief Supply Chain Officer",
        "domain": "supply chain management, procurement, logistics, vendor risk",
        "domain_fields": '"supply_chain_impact": "<str>", "vendor_dependency": "<str>", "logistics_complexity": "<str>", "procurement_needs": "<str>", "operational_risk": "low|medium|high|critical"',
    },
    "esg": {
        "role": "ESG Officer",
        "title": "ESG & Sustainability Officer",
        "domain": "environmental sustainability, social responsibility, governance, ESG reporting",
        "domain_fields": '"environmental_impact": "<str>", "social_impact": "<str>", "governance_implications": "<str>", "sustainability_score": "<str>", "esg_risk": "low|medium|high|critical"',
    },
    "ai_governance": {
        "role": "AIGO",
        "title": "AI Governance & Ethics Officer",
        "domain": "AI ethics, algorithmic fairness, responsible AI, model governance",
        "domain_fields": '"ethical_risk": "<str>", "transparency_requirements": "<str>", "governance_framework": "<str>", "societal_impact": "<str>", "ai_risk_level": "low|medium|high|critical"',
    },
    "innovation": {
        "role": "CIO-Innovation",
        "title": "Chief Innovation Officer",
        "domain": "R&D strategy, emerging technology, innovation pipeline, patents",
        "domain_fields": '"innovation_potential": "<str>", "technology_readiness": "<str>", "research_requirements": "<str>", "ip_opportunity": "<str>", "innovation_risk": "low|medium|high"',
    },
    "investor_relations": {
        "role": "IRO",
        "title": "Investor Relations Officer",
        "domain": "shareholder communication, market perception, earnings impact",
        "domain_fields": '"market_perception": "<str>", "earnings_impact": "<str>", "shareholder_value": "<str>", "communication_strategy": "<str>", "investor_sentiment": "positive|neutral|negative|mixed"',
    },
}


def build_compact_system_prompt(agent_id: str) -> str:
    """Build a compact system prompt for production use."""
    config = AGENT_COMPACT_CONFIGS[agent_id]
    return COMPACT_SYSTEM_TEMPLATE.format(**config)


def build_compact_user_prompt(scenario: str, context: str | None = None) -> str:
    """Build a minimal user prompt."""
    prompt = f"Proposal: {scenario[:800]}"
    if context:
        # Only include first 400 chars of context
        prompt += f"\n\nContext: {context[:400]}"
    return prompt
