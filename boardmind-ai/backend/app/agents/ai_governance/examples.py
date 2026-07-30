"""AI Governance & Ethics Officer example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the AI Governance Agent's output quality
2. Demonstrating the expected style of AI ethics reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    AIGovernanceAgentRequest,
    AIGovernanceAgentResponse,
    AIGovernanceDomainAssessment,
    Position,
    AIRiskLevel,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_HIRING_AI = AIGovernanceAgentRequest(
    scenario=(
        "We are deploying an AI-powered resume screening tool that will automatically "
        "filter and rank candidates for all open positions. The system uses NLP to "
        "extract skills and a neural network to predict candidate success based on "
        "historical hiring and performance data from the past 5 years."
    ),
    context=(
        "500+ positions filled annually. Historical data shows 70% male hires in "
        "technical roles. The model achieves 85% accuracy on historical outcomes. "
        "No fairness testing has been conducted. The vendor claims the system is 'unbiased'."
    ),
)

SCENARIO_CREDIT_SCORING = AIGovernanceAgentRequest(
    scenario=(
        "The lending division proposes replacing the traditional credit scoring model "
        "with a deep learning system that incorporates alternative data sources including "
        "social media activity, mobile phone usage patterns, and geolocation data to "
        "expand credit access to underbanked populations."
    ),
    context=(
        "Current model denies credit to 40% of applicants in minority zip codes. "
        "New model tested on historical data shows 15% improvement in default prediction. "
        "No disparate impact analysis conducted. Alternative data sources may serve as "
        "proxies for protected attributes."
    ),
)

SCENARIO_CONTENT_MODERATION = AIGovernanceAgentRequest(
    scenario=(
        "The platform team proposes deploying an AI content moderation system to "
        "automatically flag and remove harmful content. The system will process "
        "2 million posts daily with automated removal for high-confidence violations "
        "and human review queue for borderline cases."
    ),
    context=(
        "Current manual moderation handles 200K posts/day with 48-hour average review time. "
        "The AI system achieves 92% precision but has known performance gaps for content in "
        "non-English languages and cultural context-dependent expressions. False positive "
        "rate varies from 3% (English) to 12% (other languages)."
    ),
)

SCENARIO_PREDICTIVE_POLICING = AIGovernanceAgentRequest(
    scenario=(
        "A government client requests we develop a predictive analytics tool for "
        "resource allocation in public safety. The tool would analyze historical "
        "incident data, demographic patterns, and environmental factors to predict "
        "areas with higher probability of incidents requiring intervention."
    ),
    context=(
        "Historical data spans 10 years and reflects known over-policing patterns in "
        "minority communities. Similar tools in other jurisdictions have faced legal "
        "challenges. The client insists the tool will be 'advisory only' but deployment "
        "will directly influence resource allocation decisions."
    ),
)

SCENARIO_CUSTOMER_CHURN = AIGovernanceAgentRequest(
    scenario=(
        "The data science team proposes a customer churn prediction model that would "
        "identify at-risk customers and trigger automated retention offers including "
        "personalized pricing, service upgrades, and loyalty incentives. The model "
        "uses behavioral signals, usage patterns, and customer demographics."
    ),
    context=(
        "Model trained on 3 years of customer data (2M records). Uses 47 features "
        "including age, income bracket, and zip code. Preliminary testing shows "
        "retention offers concentrated in higher-income segments. Model will trigger "
        "automated actions without human review for standard retention offers."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_HIRING_AI = AIGovernanceAgentResponse(
    agent_id="ai_governance",
    round=1,
    position=Position.OPPOSE,
    confidence=0.85,
    domain_assessment=AIGovernanceDomainAssessment(
        ethical_risk=(
            "Critical bias risk: training data with 70% male hires in technical roles "
            "will encode gender discrimination into the model. Neural networks trained on "
            "biased historical outcomes reproduce and potentially amplify those biases. "
            "No fairness testing conducted — this is a fundamental governance failure. "
            "Vendor's 'unbiased' claim without evidence is a red flag."
        ),
        transparency_requirements=(
            "EU AI Act classifies employment AI as high-risk (Annex III). Requires: "
            "individual explanations for all rejection decisions, model documentation "
            "including training data characteristics, performance metrics disaggregated "
            "by protected attributes, and logging of all automated decisions for audit. "
            "Neural network opacity makes compliance extremely challenging."
        ),
        governance_framework=(
            "Deployment without bias testing violates NIST AI RMF 'Measure' function. "
            "No AI Ethics Board review documented. NYC Local Law 144 requires annual "
            "bias audit for automated employment decision tools. EEOC guidance on "
            "algorithmic fairness in hiring requires disparate impact testing. "
            "Current proposal meets none of these requirements."
        ),
        societal_impact=(
            "500+ hiring decisions annually affecting candidates' livelihoods. "
            "Systematic bias at this scale perpetuates workforce homogeneity and "
            "excludes qualified candidates from underrepresented groups. Reputational "
            "damage if discriminatory outcomes become public. Legal liability under "
            "Title VII for disparate impact without job-relatedness defense."
        ),
        ai_risk_level=AIRiskLevel.CRITICAL,
    ),
    summary=(
        "Oppose deployment — the hiring AI has critical unaddressed bias risks, no "
        "fairness testing, and fails to meet minimum responsible AI governance standards."
    ),
    rationale=(
        "This proposal presents unacceptable AI ethics risks in its current form. Training "
        "a neural network on 5 years of historical hiring data that reflects 70% male "
        "representation in technical roles will almost certainly encode gender bias into "
        "the model's predictions. The 85% accuracy metric is meaningless without "
        "disaggregation by protected attributes — a model can be globally accurate while "
        "being systematically unfair to specific groups.\n\n"
        "The complete absence of fairness testing is a fundamental governance failure. "
        "No responsible AI framework permits deploying a high-risk automated decision "
        "system without pre-deployment bias assessment. The vendor's unsubstantiated "
        "'unbiased' claim, without evidence of testing methodology, fairness metrics, "
        "or third-party audit, should be treated with extreme skepticism.\n\n"
        "From a regulatory perspective, this system falls squarely within high-risk AI "
        "classification under the EU AI Act (employment decisions) and would require "
        "annual bias audits under NYC Local Law 144. Deploying without these safeguards "
        "exposes the organization to regulatory action, litigation under Title VII, and "
        "severe reputational damage. I cannot support deployment until comprehensive "
        "fairness testing demonstrates equitable outcomes across all protected attributes."
    ),
    risks=[
        "Gender bias encoded from 70% male training data — model likely systematically disadvantages female and non-binary candidates",
        "Regulatory non-compliance: EU AI Act high-risk requirements, NYC LL144 bias audit mandate, EEOC algorithmic fairness guidance",
        "Legal liability under Title VII for disparate impact in automated hiring without validated job-relatedness defense",
        "Reputational catastrophe if biased outcomes become public — similar tools have generated significant negative press",
    ],
    conditions=[
        "Halt deployment until comprehensive bias audit across gender, race, age, and disability is completed with published results",
        "Require vendor to provide fairness metrics (demographic parity, equalized odds) disaggregated by all protected attributes",
        "Implement human-in-the-loop review for all rejection decisions with documented override capability",
        "Establish ongoing monitoring with monthly fairness metric reporting and defined intervention thresholds",
    ],
    metrics_to_track=[
        "Selection rate ratio across protected groups — must meet 4/5ths rule (80% rule) minimum",
        "False negative rate by demographic group — candidates incorrectly rejected",
        "Human override rate — frequency of reviewers changing AI decisions",
        "Adverse impact ratio — quarterly disparate impact analysis",
        "Candidate experience feedback disaggregated by demographics",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_CONTENT_MODERATION = AIGovernanceAgentResponse(
    agent_id="ai_governance",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.7,
    domain_assessment=AIGovernanceDomainAssessment(
        ethical_risk=(
            "Moderate bias risk: 4x higher false positive rate for non-English content "
            "(12% vs 3%) creates disparate silencing of non-English speaking communities. "
            "Cultural context gaps may misclassify legitimate expression. Automated "
            "removal without appeal mechanism violates proportionality principles."
        ),
        transparency_requirements=(
            "Users must be notified of AI involvement in content decisions. Appeal "
            "mechanism required for all automated removals. Transparency report "
            "must include disaggregated accuracy metrics by language and content type. "
            "Explainability needed for borderline decisions in human review queue."
        ),
        governance_framework=(
            "Content moderation AI classified as medium-risk under EU AI Act. "
            "Digital Services Act requires transparency in automated content decisions. "
            "Santa Clara Principles on transparency and accountability in content "
            "moderation provide baseline governance framework. Regular third-party "
            "audit of decision patterns required."
        ),
        societal_impact=(
            "2 million posts daily — scale means even small error rates affect thousands. "
            "Unequal performance across languages raises equity and digital inclusion concerns. "
            "Over-moderation chills legitimate speech; under-moderation enables harm. "
            "Balance requires ongoing calibration with community input."
        ),
        ai_risk_level=AIRiskLevel.MEDIUM,
    ),
    summary=(
        "Conditionally support with mandatory language equity improvements — the 4x "
        "false positive disparity must be reduced before full automated deployment."
    ),
    rationale=(
        "Content moderation at scale requires AI assistance — 2 million posts daily cannot "
        "be reviewed manually. The 92% precision for English content is acceptable for "
        "high-confidence automated removal. However, the 12% false positive rate for "
        "non-English content represents a significant equity concern that creates "
        "disproportionate silencing of non-English speaking communities.\n\n"
        "The governance framework should implement a tiered approach: automated removal "
        "only for high-confidence, language-agnostic violations (e.g., known CSAM hashes, "
        "previously identified terrorist content), while borderline and context-dependent "
        "decisions go to human review. The human review queue must prioritize non-English "
        "content given the higher error rate.\n\n"
        "I support deployment on the condition that the language performance gap is "
        "addressed within a defined timeline, appeal mechanisms are available for all "
        "automated decisions, and transparency reporting disaggregates metrics by "
        "language to enable ongoing accountability. Regular third-party audits should "
        "assess both over- and under-moderation patterns."
    ),
    risks=[
        "Language-based discrimination: 4x higher false positive rate for non-English speakers constitutes inequitable treatment",
        "Over-moderation chilling effect on legitimate speech — automated systems cannot reliably assess cultural context and nuance",
        "Lack of appeal mechanism for automated removals violates procedural fairness and potentially the Digital Services Act",
        "Feedback loop risk: if moderation decisions influence training data, current biases become self-reinforcing",
    ],
    conditions=[
        "Reduce non-English false positive rate to within 2x of English rate (target <6%) before full automated deployment",
        "Implement appeal mechanism with human review guarantee within 24 hours for all automated removals",
        "Publish quarterly transparency report with accuracy metrics disaggregated by language and content type",
        "Conduct bi-annual third-party audit of moderation patterns with published findings",
    ],
    metrics_to_track=[
        "False positive rate by language — target convergence to <2x disparity",
        "Appeal rate and overturn rate — monitor for systematic errors",
        "Time to human review for borderline cases — target <4 hours",
        "Content removal distribution by language and user demographics",
        "User satisfaction with moderation decisions — quarterly survey",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("AI Hiring Screening", SCENARIO_HIRING_AI),
    ("AI Credit Scoring", SCENARIO_CREDIT_SCORING),
    ("AI Content Moderation", SCENARIO_CONTENT_MODERATION),
    ("Predictive Policing", SCENARIO_PREDICTIVE_POLICING),
    ("Customer Churn Prediction", SCENARIO_CUSTOMER_CHURN),
]

ALL_EXAMPLE_RESPONSES = [
    ("AI Hiring Screening", EXAMPLE_RESPONSE_HIRING_AI),
    ("AI Content Moderation", EXAMPLE_RESPONSE_CONTENT_MODERATION),
]
