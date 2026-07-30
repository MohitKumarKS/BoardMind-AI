"""Chief Innovation Officer example scenarios and expected responses.

These examples serve multiple purposes:
1. Testing the Innovation Agent's output quality
2. Demonstrating the expected style of innovation reasoning
3. Providing few-shot examples for prompt engineering if needed
4. Documenting the agent's behavior for the team
"""

from .schema import (
    InnovationAgentRequest,
    InnovationAgentResponse,
    InnovationDomainAssessment,
    Position,
    InnovationRiskLevel,
)


# --- Example Scenarios (Inputs) ---

SCENARIO_QUANTUM_COMPUTING = InnovationAgentRequest(
    scenario=(
        "We are considering establishing a quantum computing research lab to develop "
        "quantum-resistant cryptographic algorithms and explore quantum optimization "
        "for our supply chain operations. The initiative would require hiring 5 quantum "
        "researchers and investing in cloud-based quantum computing access."
    ),
    context=(
        "Current R&D budget: $8M annually. No existing quantum expertise in-house. "
        "Three competitors have announced quantum research initiatives. NIST post-quantum "
        "cryptography standards expected to be mandated within 3-5 years. Our cryptographic "
        "infrastructure protects $4B in annual transaction volume."
    ),
)

SCENARIO_GENERATIVE_AI_PLATFORM = InnovationAgentRequest(
    scenario=(
        "The product team proposes building a proprietary generative AI platform that "
        "fine-tunes foundation models on our domain-specific data to create specialized "
        "AI assistants for our enterprise customers. This would differentiate us from "
        "competitors using generic AI APIs."
    ),
    context=(
        "We have 10 years of proprietary domain data (2PB). Current product uses third-party "
        "AI APIs costing $45K/month. Three competitors launched similar offerings in the last "
        "6 months. Our enterprise customers increasingly ask for AI features — 65% mentioned "
        "it in recent surveys."
    ),
)

SCENARIO_BIOTECH_PARTNERSHIP = InnovationAgentRequest(
    scenario=(
        "A university research lab has approached us about commercializing their novel "
        "protein folding prediction algorithm. Their approach outperforms AlphaFold on "
        "certain protein families by 15-20% accuracy. They seek an exclusive licensing "
        "deal with co-development obligations."
    ),
    context=(
        "We have no current biotech products but adjacent computational biology expertise. "
        "The protein folding market is projected at $3.2B by 2028. The university wants "
        "$2M upfront + 8% royalties. Their team of 4 PhD researchers would need industry "
        "engineering support to productionize."
    ),
)

SCENARIO_EDGE_AI_HARDWARE = InnovationAgentRequest(
    scenario=(
        "The engineering team proposes designing a custom AI inference chip optimized for "
        "our specific workloads. Initial analysis suggests 10x performance improvement "
        "over general-purpose GPUs for our model architectures, with 5x power efficiency "
        "gains. The chip would take 24-30 months to tape out."
    ),
    context=(
        "Current GPU spend: $12M/year and growing 40% annually. Custom chip development "
        "estimated at $50-80M total investment. We process 2B inferences daily. Three "
        "well-funded startups are developing similar domain-specific AI chips. Our models "
        "have unique architectural characteristics that generic chips handle inefficiently."
    ),
)

SCENARIO_AR_PRODUCT_LINE = InnovationAgentRequest(
    scenario=(
        "Innovation team proposes creating an augmented reality product line for "
        "industrial maintenance and training. Early prototypes show 40% reduction "
        "in maintenance errors and 60% faster technician onboarding when using AR "
        "guidance overlays in field service operations."
    ),
    context=(
        "Field service operations cover 50,000+ annual maintenance visits. Current "
        "error rate: 12%. Training time for new technicians: 6 months. AR hardware "
        "costs have dropped 60% in the last 2 years. Two industrial competitors "
        "have announced AR pilot programs."
    ),
)


# --- Example Responses (Expected Output Style) ---

EXAMPLE_RESPONSE_QUANTUM = InnovationAgentResponse(
    agent_id="innovation",
    round=1,
    position=Position.CONDITIONAL,
    confidence=0.7,
    domain_assessment=InnovationDomainAssessment(
        innovation_potential=(
            "High strategic innovation value. Quantum-resistant cryptography is a defensive "
            "necessity (NIST mandate in 3-5 years), while quantum optimization represents "
            "offensive differentiation opportunity. First-mover advantage possible in "
            "domain-specific quantum applications for supply chain optimization. "
            "Horizon 3 innovation with 5-10 year full realization timeline."
        ),
        technology_readiness=(
            "Quantum-resistant crypto: TRL 6-7 (NIST algorithms selected and available). "
            "Quantum optimization for supply chain: TRL 2-3 (theoretical feasibility "
            "demonstrated, no practical advantage yet at relevant scale). Cloud quantum "
            "access available but current hardware limited to ~1000 qubits with high "
            "error rates — meaningful advantage requires fault-tolerant quantum computing "
            "(estimated 5-8 years)."
        ),
        research_requirements=(
            "Phase 1 (Crypto Migration): $1.5M over 12 months, 3 cryptography specialists. "
            "This is engineering, not research — well-understood path. "
            "Phase 2 (Quantum Optimization R&D): $3-5M over 36 months, 5 quantum researchers "
            "with PhD-level expertise. University partnerships essential for talent pipeline. "
            "Cloud quantum computing access: $200-400K/year."
        ),
        ip_opportunity=(
            "Limited patent opportunity in quantum-resistant crypto (NIST standards are public). "
            "Strong IP potential in domain-specific quantum optimization algorithms — "
            "supply chain quantum formulations are largely unexplored. Estimated 3-6 "
            "patentable innovations in quantum algorithm design for logistics optimization. "
            "Trade secret protection viable for proprietary quantum circuit designs."
        ),
        innovation_risk=InnovationRiskLevel.HIGH,
    ),
    summary=(
        "Conditionally support with bifurcated strategy — accelerate crypto migration "
        "(defensive necessity) while funding exploratory quantum optimization R&D with "
        "clear stage gates."
    ),
    rationale=(
        "This proposal conflates two distinct initiatives with very different risk profiles "
        "and timelines. Quantum-resistant cryptography migration is not truly innovation — "
        "it is a defensive engineering necessity with NIST standards already selected. This "
        "should be treated as a security infrastructure project and accelerated given the "
        "3-5 year mandate timeline and our $4B transaction exposure.\n\n"
        "Quantum optimization for supply chain, however, is genuine Horizon 3 innovation "
        "with high uncertainty. Current quantum hardware cannot deliver practical advantage "
        "over classical optimization at our scale. The research value lies in developing "
        "algorithms and expertise now so we are positioned to exploit quantum advantage "
        "when hardware matures (estimated 5-8 years). This is a valid R&D bet if sized "
        "appropriately.\n\n"
        "I recommend bifurcating the initiative: fast-track crypto migration as an "
        "engineering project (12 months, $1.5M) while establishing a focused quantum "
        "optimization research program with annual go/no-go reviews based on hardware "
        "advancement milestones. The research program should target 2-3 specific supply "
        "chain problems where quantum formulation advantage is theoretically established, "
        "and publish results to attract talent and establish thought leadership."
    ),
    risks=[
        "Quantum optimization may not achieve practical advantage over classical methods for 5-8 years — research investment has long and uncertain payback",
        "Talent acquisition extremely competitive — quantum researchers command $300-500K compensation and have many competing offers",
        "Technology pivot risk: quantum hardware architecture is not settled — algorithms developed for current paradigms may not transfer",
        "Competitor timing: if we start too early, we burn budget; if too late, we cannot catch up on expertise when hardware matures",
    ],
    conditions=[
        "Separate crypto migration (engineering) from quantum optimization (research) with independent budgets and timelines",
        "Establish annual review gate for quantum optimization: continue/pivot/terminate based on hardware advancement milestones",
        "Secure at least 2 PhD-level quantum researchers before committing Phase 2 budget — talent is the binding constraint",
        "Establish 2+ university research partnerships to supplement internal team and provide talent pipeline",
    ],
    metrics_to_track=[
        "Crypto migration progress — percentage of systems transitioned to post-quantum algorithms",
        "Quantum algorithm development — number of domain-specific formulations achieving theoretical quantum advantage",
        "Publication and patent output — research quality indicator and talent attractor",
        "Hardware advancement tracking — monitor qubit count, error rates, and coherence times against roadmap assumptions",
        "Talent pipeline — applications received, offers accepted, retention rate for quantum team",
    ],
    references_to=[],
)

EXAMPLE_RESPONSE_AR_PRODUCT = InnovationAgentResponse(
    agent_id="innovation",
    round=1,
    position=Position.SUPPORT,
    confidence=0.8,
    domain_assessment=InnovationDomainAssessment(
        innovation_potential=(
            "High innovation potential with validated prototype results. 40% error reduction "
            "and 60% faster onboarding represent substantial operational improvements with "
            "clear commercial value. First-mover advantage accessible given competitors are "
            "only at pilot stage. Horizon 2 innovation: adjacent to core business with "
            "proven technology applied in novel context."
        ),
        technology_readiness=(
            "TRL 6-7: system prototype demonstrated in relevant operational environment "
            "with positive results. AR hardware is mature (TRL 9) with declining costs "
            "(60% reduction in 2 years). Software overlay and guidance systems at TRL 6 — "
            "field-validated but requiring productionization for scale deployment. "
            "12-month path to production-ready product (TRL 8-9)."
        ),
        research_requirements=(
            "Limited research needed — primarily engineering and productionization. "
            "Estimated $2-3M over 12 months: 6 AR/computer vision engineers, UX designer "
            "for industrial interfaces, field testing team. Hardware procurement for "
            "pilot fleet: $500K. Key challenge is content creation at scale — 50K+ "
            "maintenance procedures need AR overlay development."
        ),
        ip_opportunity=(
            "2-3 patentable innovations in AR overlay generation from maintenance manuals "
            "and real-time equipment state detection. Strong trade secret opportunity in "
            "domain-specific computer vision models. Defensive patent filing recommended "
            "given competitor activity. Content creation automation pipeline is key "
            "differentiator with strong IP protection potential."
        ),
        innovation_risk=InnovationRiskLevel.LOW,
    ),
    summary=(
        "Strongly support — validated prototype with compelling metrics, mature underlying "
        "technology, and clear first-mover window make this a high-confidence innovation bet."
    ),
    rationale=(
        "This is a textbook Horizon 2 innovation opportunity: proven technology (AR hardware) "
        "applied in a novel context (industrial maintenance) with validated prototype results "
        "demonstrating substantial value creation. The 40% error reduction and 60% onboarding "
        "acceleration are not theoretical — they are measured in operational conditions. This "
        "dramatically de-risks the initiative.\n\n"
        "The technology readiness is unusually high for an innovation proposal. AR hardware "
        "is commercially mature and declining in cost. The remaining engineering challenge "
        "is primarily software: building the guidance overlay system, equipment recognition, "
        "and content creation pipeline for 50K+ maintenance procedures. This is achievable "
        "with a strong engineering team in 12 months.\n\n"
        "The competitive window is open but closing. Competitors are at pilot stage — we have "
        "a 6-12 month advantage with our validated prototype. The IP strategy should "
        "prioritize rapid provisional patent filings on our novel approaches to AR content "
        "generation and real-time equipment state detection. The combination of validated "
        "results, mature technology, and accessible first-mover position makes this one of "
        "the strongest innovation opportunities in our current pipeline."
    ),
    risks=[
        "Content creation scale challenge — generating AR overlays for 50K+ procedures is labor-intensive without automation breakthrough",
        "Field adoption resistance — technicians may resist AR hardware in harsh environments; ergonomics and durability are concerns",
        "Competitor acceleration — 6-12 month advantage is perishable if competitors secure similar prototype validation",
        "Hardware dependency — single-vendor AR hardware creates supply chain and technology lock-in risk",
    ],
    conditions=[
        "Validate AR content creation automation approach within first 3 months — this is the scaling bottleneck",
        "Conduct field acceptance testing with 50+ technicians across diverse environments before full-scale commitment",
        "File provisional patents on novel AR overlay generation and equipment detection methods within 60 days",
        "Establish multi-vendor AR hardware strategy to avoid platform lock-in",
    ],
    metrics_to_track=[
        "Maintenance error rate with AR vs. without — target sustained 40%+ reduction at scale",
        "Technician onboarding time — measure from hire to independent operation with AR assist",
        "AR content coverage — percentage of maintenance procedures with active AR overlays",
        "Field adoption rate — percentage of technicians actively using AR in daily operations",
        "Patent filings — target 3+ provisional applications within 6 months",
    ],
    references_to=[],
)


# Collect all scenarios for easy iteration
ALL_SCENARIOS = [
    ("Quantum Computing Research", SCENARIO_QUANTUM_COMPUTING),
    ("Generative AI Platform", SCENARIO_GENERATIVE_AI_PLATFORM),
    ("Biotech Partnership", SCENARIO_BIOTECH_PARTNERSHIP),
    ("Edge AI Hardware", SCENARIO_EDGE_AI_HARDWARE),
    ("AR Product Line", SCENARIO_AR_PRODUCT_LINE),
]

ALL_EXAMPLE_RESPONSES = [
    ("Quantum Computing Research", EXAMPLE_RESPONSE_QUANTUM),
    ("AR Product Line", EXAMPLE_RESPONSE_AR_PRODUCT),
]
