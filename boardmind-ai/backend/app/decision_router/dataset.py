"""Decision Router training dataset.

Contains representative business scenarios for each category.
The dataset is used to train the TF-IDF + classifier pipeline.
It can be expanded over time without changing any other module.
"""

TRAINING_DATA: list[tuple[str, str]] = [
    # --- product_launch ---
    ("We are planning to launch a new SaaS product targeting enterprise customers", "product_launch"),
    ("The team wants to release a mobile app for our existing platform", "product_launch"),
    ("We are considering bringing a new AI-powered feature to market", "product_launch"),
    ("Should we launch a freemium version of our software", "product_launch"),
    ("Planning a new product line targeting mid-market companies", "product_launch"),
    ("We want to introduce a self-service tier for small businesses", "product_launch"),
    ("The product team proposes launching a developer API as a standalone product", "product_launch"),
    ("We are developing a new hardware product and need to plan the go-to-market", "product_launch"),
    ("Should we build and launch a companion app for our main product", "product_launch"),
    ("Evaluating whether to launch our internal tool as a commercial product", "product_launch"),

    # --- market_expansion ---
    ("We want to expand into the European market starting with UK and Germany", "market_expansion"),
    ("Considering entering the Asia-Pacific market for our B2B product", "market_expansion"),
    ("Should we expand from enterprise into the mid-market segment", "market_expansion"),
    ("Planning geographic expansion into Latin American markets", "market_expansion"),
    ("We want to open operations in a new country", "market_expansion"),
    ("Evaluating expansion into the healthcare vertical", "market_expansion"),
    ("Should we enter the government sector with our existing product", "market_expansion"),
    ("Planning to expand our distribution into retail channels", "market_expansion"),
    ("We are looking to expand our services into the education sector", "market_expansion"),
    ("Considering opening a branch office in Singapore to serve APAC", "market_expansion"),

    # --- pricing_strategy ---
    ("We are considering raising prices by 20% for new customers", "pricing_strategy"),
    ("Should we switch from monthly to annual billing only", "pricing_strategy"),
    ("Evaluating a usage-based pricing model instead of flat subscription", "pricing_strategy"),
    ("The team proposes introducing a premium enterprise tier at 3x current price", "pricing_strategy"),
    ("Should we offer volume discounts for larger contracts", "pricing_strategy"),
    ("Considering a freemium model with paid upgrades", "pricing_strategy"),
    ("We need to restructure our pricing tiers to reduce churn", "pricing_strategy"),
    ("Finance wants to increase renewal prices by 15% across the board", "pricing_strategy"),
    ("Should we bundle multiple products into a single pricing package", "pricing_strategy"),
    ("Evaluating competitive pricing response after a competitor dropped prices 30%", "pricing_strategy"),

    # --- hiring ---
    ("We need to hire 10 engineers in the next quarter", "hiring"),
    ("Planning to build a new data science team from scratch", "hiring"),
    ("Should we hire a VP of Engineering or promote internally", "hiring"),
    ("The sales team wants to add 5 account executives this quarter", "hiring"),
    ("We need to recruit a Chief Marketing Officer", "hiring"),
    ("Planning to hire 20 people for our new offshore development center", "hiring"),
    ("Should we bring on contract developers or hire full-time engineers", "hiring"),
    ("We want to double our customer success team in 6 months", "hiring"),
    ("Evaluating whether to hire a dedicated security team", "hiring"),
    ("Need to recruit senior leadership for our new business unit", "hiring"),

    # --- infrastructure_upgrade ---
    ("We need to upgrade our database infrastructure to handle 10x traffic", "infrastructure_upgrade"),
    ("Planning to migrate from on-premise to cloud infrastructure", "infrastructure_upgrade"),
    ("Should we invest in a GPU cluster for machine learning workloads", "infrastructure_upgrade"),
    ("Our CI/CD pipeline needs a complete overhaul", "infrastructure_upgrade"),
    ("Evaluating migration from AWS to Google Cloud Platform", "infrastructure_upgrade"),
    ("We need to upgrade our network infrastructure across all offices", "infrastructure_upgrade"),
    ("Planning to implement a new data warehouse solution", "infrastructure_upgrade"),
    ("Should we rebuild our monolith into microservices", "infrastructure_upgrade"),
    ("Our servers are reaching end of life and need replacement", "infrastructure_upgrade"),
    ("Considering investing in dedicated AI inference infrastructure", "infrastructure_upgrade"),

    # --- digital_transformation ---
    ("We want to automate our entire customer onboarding process", "digital_transformation"),
    ("Planning to implement AI across all customer touchpoints", "digital_transformation"),
    ("Should we digitize our paper-based approval workflows", "digital_transformation"),
    ("The company needs a complete digital transformation of operations", "digital_transformation"),
    ("We want to implement an AI copilot for internal productivity", "digital_transformation"),
    ("Planning to replace legacy systems with modern cloud-native solutions", "digital_transformation"),
    ("Should we adopt robotic process automation for back-office functions", "digital_transformation"),
    ("We need to transform our sales process with AI-driven tools", "digital_transformation"),
    ("Evaluating enterprise-wide adoption of generative AI tools", "digital_transformation"),
    ("Planning to automate financial reporting and compliance monitoring", "digital_transformation"),

    # --- compliance ---
    ("We need to become GDPR compliant before serving European customers", "compliance"),
    ("Planning to achieve SOC 2 Type II certification", "compliance"),
    ("Should we implement HIPAA compliance to enter healthcare market", "compliance"),
    ("Our data handling practices need review for CCPA compliance", "compliance"),
    ("We need to establish a formal data governance framework", "compliance"),
    ("Planning to implement anti-money laundering controls", "compliance"),
    ("Should we hire a Data Protection Officer for GDPR obligations", "compliance"),
    ("We need to audit our vendor contracts for compliance gaps", "compliance"),
    ("Evaluating our readiness for upcoming AI regulation requirements", "compliance"),
    ("Need to implement accessibility compliance across our product", "compliance"),

    # --- marketing_campaign ---
    ("We want to launch a major brand awareness campaign in Q4", "marketing_campaign"),
    ("Planning a product launch marketing campaign with $500K budget", "marketing_campaign"),
    ("Should we invest heavily in content marketing and SEO", "marketing_campaign"),
    ("Evaluating a partnership marketing campaign with an industry influencer", "marketing_campaign"),
    ("We want to run a demand generation campaign targeting CTOs", "marketing_campaign"),
    ("Planning a rebranding campaign to reposition as premium", "marketing_campaign"),
    ("Should we sponsor a major industry conference as lead sponsor", "marketing_campaign"),
    ("We want to launch an account-based marketing program for top 50 accounts", "marketing_campaign"),
    ("Planning a viral social media campaign to drive consumer awareness", "marketing_campaign"),
    ("Evaluating a referral marketing program to reduce CAC", "marketing_campaign"),

    # --- sales_strategy ---
    ("We want to shift from outbound to inbound-led sales motion", "sales_strategy"),
    ("Planning to implement a channel partner sales program", "sales_strategy"),
    ("Should we create a dedicated enterprise sales team separate from mid-market", "sales_strategy"),
    ("Evaluating whether to add a self-service sales channel", "sales_strategy"),
    ("We want to restructure sales territories for better coverage", "sales_strategy"),
    ("Planning to implement a product-led growth sales motion", "sales_strategy"),
    ("Should we invest in a sales development representative team", "sales_strategy"),
    ("We need to redesign our sales compensation plan to drive growth", "sales_strategy"),
    ("Evaluating a land-and-expand strategy for enterprise accounts", "sales_strategy"),
    ("We want to build a reseller channel in addition to direct sales", "sales_strategy"),

    # --- cost_optimization ---
    ("We need to reduce operational costs by 25% this year", "cost_optimization"),
    ("Should we consolidate our vendor relationships to save money", "cost_optimization"),
    ("Planning to optimize cloud infrastructure spend which has grown 40%", "cost_optimization"),
    ("We want to reduce customer acquisition costs through efficiency", "cost_optimization"),
    ("Evaluating whether to outsource non-core functions to reduce overhead", "cost_optimization"),
    ("Need to find $2M in annual savings without reducing headcount", "cost_optimization"),
    ("Should we renegotiate all SaaS vendor contracts for better rates", "cost_optimization"),
    ("Planning to implement zero-based budgeting across departments", "cost_optimization"),
    ("We need to reduce our burn rate by 30% to extend runway", "cost_optimization"),
    ("Evaluating shared services model to reduce duplicated costs", "cost_optimization"),

    # --- business_acquisition ---
    ("We are considering acquiring a startup for their AI technology", "business_acquisition"),
    ("Should we acquire our main competitor who is struggling financially", "business_acquisition"),
    ("Evaluating a merger with a complementary company in our space", "business_acquisition"),
    ("We want to acqui-hire a 15-person engineering team", "business_acquisition"),
    ("Planning to acquire a company for their customer base and distribution", "business_acquisition"),
    ("Should we pursue a strategic acquisition to enter a new vertical", "business_acquisition"),
    ("Evaluating buying a smaller competitor to consolidate market share", "business_acquisition"),
    ("We have an opportunity to acquire a key technology vendor", "business_acquisition"),
    ("Considering a reverse merger to accelerate our path to IPO", "business_acquisition"),
    ("Should we acquire a company for their patent portfolio", "business_acquisition"),

    # --- operational_improvement ---
    ("We need to reduce our deployment time from 2 weeks to 2 days", "operational_improvement"),
    ("Planning to implement a new project management framework", "operational_improvement"),
    ("Should we adopt agile methodology across all teams", "operational_improvement"),
    ("We want to improve our customer support response time by 50%", "operational_improvement"),
    ("Need to streamline our procurement process which takes too long", "operational_improvement"),
    ("Planning to implement continuous deployment for faster releases", "operational_improvement"),
    ("Should we reorganize teams around product lines instead of functions", "operational_improvement"),
    ("We need to improve cross-team coordination and reduce handoff delays", "operational_improvement"),
    ("Evaluating lean manufacturing principles for our operations", "operational_improvement"),
    ("We want to reduce order fulfillment time from 5 days to same-day", "operational_improvement"),

    # --- customer_experience ---
    ("We want to completely redesign our customer onboarding experience", "customer_experience"),
    ("Planning to implement a self-service portal for customer account management", "customer_experience"),
    ("Should we invest in a customer health score and proactive success program", "customer_experience"),
    ("We need to improve our NPS score which has dropped 15 points", "customer_experience"),
    ("Evaluating implementation of an AI chatbot for 24/7 customer support", "customer_experience"),
    ("We want to create a unified customer experience across all channels", "customer_experience"),
    ("Planning to build a customer community platform for engagement", "customer_experience"),
    ("Should we redesign our product UX based on customer feedback", "customer_experience"),
    ("We need to reduce customer effort score in our support process", "customer_experience"),
    ("Evaluating a loyalty program to increase retention and lifetime value", "customer_experience"),

    # --- general_strategic_decision ---
    ("Should we pivot our business model from B2B to B2C", "general_strategic_decision"),
    ("We need to decide our company strategy for the next 3 years", "general_strategic_decision"),
    ("Evaluating whether to take venture capital funding or bootstrap", "general_strategic_decision"),
    ("Should we go public via IPO or remain private", "general_strategic_decision"),
    ("We are deciding whether to focus on growth or profitability this year", "general_strategic_decision"),
    ("Planning our annual strategic priorities and resource allocation", "general_strategic_decision"),
    ("Should we spin off a business unit into a separate company", "general_strategic_decision"),
    ("We need to decide our response to a major market disruption", "general_strategic_decision"),
    ("Evaluating a fundamental change to our go-to-market model", "general_strategic_decision"),
    ("The board wants to discuss our long-term competitive positioning", "general_strategic_decision"),
]
