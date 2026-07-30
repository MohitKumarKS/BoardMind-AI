# BoardMind AI V2 — Enterprise Architecture Audit & Expansion Plan

## PHASE 1: PROJECT AUDIT

---

### 1. Architecture Overview

#### Folder Structure
```
backend/app/
├── main.py                       # FastAPI app entry point
├── __init__.py
├── agents/                       # Department agents (20 implemented)
│   ├── finance/                  # Reference agent pattern
│   │   ├── schema.py            # Pydantic models (Request/Response/DomainAssessment)
│   │   ├── service.py           # Agent service (analyze → LLM → validate)
│   │   ├── prompt.py            # System prompt + prompt builder
│   │   ├── examples.py          # Example scenarios and expected outputs
│   │   └── __init__.py          # Public exports
│   ├── marketing/, sales/, hr/, operations/, legal/, it/, business_analytics/
│   ├── ceo/, ciso/, risk/, compliance/, strategy/, product/
│   ├── customer_success/, supply_chain/, esg/, ai_governance/
│   ├── innovation/, investor_relations/
│   ├── llm_provider.py          # Multi-backend LLM abstraction
│   ├── retry.py                 # Shared retry + fallback to mock
│   ├── response_normalizer.py   # Fix LLM output quirks before validation
│   ├── evidence_extractor.py    # Extract facts from MCP data for mocks
│   └── evidence.py              # Shared prompt builder with evidence injection
├── orchestrator/                 # Wave-based multi-agent coordinator
│   ├── schema.py               # OrchestratorRequest/Response schemas
│   └── service.py              # ExecutiveOrchestratorService
├── decision_router/             # ML scenario classifier
│   ├── dataset.py              # 140 training samples (14 categories)
│   ├── training.py             # TF-IDF + CalibratedClassifierCV pipeline
│   ├── labels.py               # Category → agent mapping
│   ├── schema.py               # Request/Response schemas
│   └── service.py              # DecisionRouterService
├── consensus/                   # Deterministic consensus engine
│   ├── schema.py               # ConsensusRequest
│   └── service.py              # ConsensusEngineService (no LLM)
├── board_context/               # In-memory session state
│   ├── schema.py               # BoardContext, AgentResult, ConsensusResult
│   └── service.py              # BoardContextService (async-safe store)
├── reports/                     # PDF/JSON report generation
│   ├── schema.py               # ExecutiveReport, DepartmentEntry
│   └── service.py              # ReportGeneratorService (fpdf2)
├── routes/                      # FastAPI route modules
│   ├── boardroom.py            # POST /orchestrate, /consensus
│   ├── workspace.py            # Individual agent analysis endpoints
│   ├── agents.py               # GET /agents (list)
│   ├── reports.py              # GET /reports/{session_id}
│   ├── mcp.py                  # POST /mcp/upload
│   ├── knowledge_hub.py        # History, search, evidence retrieval
│   ├── decision_router.py      # POST /decision-router/classify
│   └── sessions.py             # Session management
├── mcp/                         # MCP tool implementations
│   ├── registry.py             # Central tool registry with usage tracking
│   ├── summarizer.py           # Convert raw data → structured evidence
│   ├── spreadsheet/service.py  # CSV/Excel reader
│   ├── filesystem/service.py   # Text/PDF/DOCX reader
│   ├── database/service.py     # SQLite query executor
│   └── websearch/service.py    # Web search (stub)
├── mcp_hub/                     # PostgreSQL persistence (optional)
│   ├── config.py               # Database URL config
│   ├── database.py             # SQLAlchemy async engine
│   ├── models.py               # Meeting, ExecutiveAnalysis, ConsensusRecord, Evidence
│   ├── storage_service.py      # CRUD for meetings/analyses/consensus
│   ├── evidence_service.py     # Domain evidence retrieval
│   ├── history_service.py      # Historical meeting search
│   └── integration.py          # Hook into main pipeline (post-consensus)
└── models/
    └── schemas.py              # Shared enums (Position, SessionStatus, etc.)
```

#### Agent Architecture Pattern (per agent)
Every agent follows this identical 5-file structure:
- **schema.py**: Position enum, domain-specific RiskLevel enum, DomainAssessment model, AgentResponse model, AgentRequest model
- **service.py**: Service class with `analyze()` → checks LLM → builds prompt → calls `retry_llm_call()` → `_parse_and_validate()` → `_generate_mock_response()` fallback
- **prompt.py**: `SYSTEM_PROMPT` constant (scope/out-of-scope/rules/JSON template), `build_X_prompt()` using shared `format_prompt_with_evidence()`
- **examples.py**: 3-5 example scenarios + 1-2 example responses for testing/documentation
- **__init__.py**: Exports Service, Request, Response, DomainAssessment, Position, RiskLevel, LLMError

#### Decision Router
- **Algorithm**: TF-IDF vectorizer (bigrams, 5000 features) + CalibratedClassifierCV(LinearSVC)
- **Training**: 140 samples across 14 business categories, trained once at module load
- **Expansion**: Keyword-based agent expansion for multi-domain scenarios
- **Output**: (category, confidence, recommended_agents, reason)

#### Orchestrator
- **Pattern**: Wave-based scheduling (WAVE_SIZE=4, parallel within wave, sequential between)
- **Rate limiting**: 5s base inter-wave delay, +12s on 429 detection
- **Timeout**: 60s per agent, graceful failure (doesn't crash session)
- **Board Context**: In-memory session store, MAX_SESSIONS=200, LRU eviction
- **Evidence filtering**: Domain-keyword matching to reduce token usage per agent

#### Consensus Engine
- **Deterministic** — no LLM calls
- **Rules**: support_ratio > 0.7 → approved, oppose_ratio > 0.5 → rejected, else conditional/review
- **Conflict detection**: Any (supporter, opposer) pair triggers conflict flag
- **Aggregation**: Risks capped at 15, actions at 20, deduplicated by prefix

#### LLM Provider
- **Primary**: Groq (llama-3.1-8b-instant) with fallback to llama-3.3-70b-versatile
- **Secondary**: OpenAI-compatible via httpx
- **Mock**: Auto-activates when no API key configured
- **Concurrency**: asyncio.Semaphore(2) — global, shared across ALL agents

#### Evidence System
- **MCP Registry**: Central tool access (spreadsheet, filesystem, database, websearch)
- **Summarizer**: Converts raw data → structured business metrics text
- **Evidence injection**: Appended to agent prompts under "Evidence From Uploaded Data"
- **Domain filtering**: Orchestrator filters evidence lines by agent-specific keywords

#### Report Generation
- **Format**: PDF (fpdf2) and JSON
- **Content**: Executive summary, department table, consensus, risks, actions, statistics, MCP sources
- **Persistence**: Optional PostgreSQL storage (base64-encoded PDF)

#### API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/boardroom/orchestrate | POST | Full multi-agent orchestration |
| /api/boardroom/consensus | POST | Run consensus on completed session |
| /api/workspace/{agent} | POST | Single agent analysis (8 endpoints) |
| /api/decision-router/classify | POST | Classify scenario only |
| /api/agents/ | GET | List available agents |
| /api/reports/{session_id} | GET | Download report (JSON/PDF) |
| /api/mcp/upload | POST | Upload file for evidence extraction |
| /api/knowledge-hub/history | GET | Past meeting history |
| /api/knowledge-hub/session/{id} | GET | Session detail |
| /api/knowledge-hub/search | GET | Search similar meetings |
| /api/knowledge-hub/evidence/{agent} | GET | Agent-specific evidence |
| /api/health | GET | Health check |

---

### 2. Request Flow Through the System

```
User submits scenario via POST /api/boardroom/orchestrate
    │
    ▼
┌─────────────────────────────┐
│  Decision Router             │
│  TF-IDF classifies scenario │
│  + keyword expansion         │
│  Returns: category, agents   │
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  Board Context Created       │
│  Session ID, scenario,       │
│  selected_agents, status     │
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────────────────────┐
│  WAVE-BASED EXECUTION                        │
│                                              │
│  Wave 1: [agent_1, agent_2, agent_3, agent_4]  (parallel)
│           ↓ 5s delay ↓
│  Wave 2: [agent_5, agent_6, agent_7, agent_8]  (parallel)
│           ↓ 5s delay ↓
│  Wave N: [remaining agents]                     (parallel)
│                                              │
│  Per Agent:                                   │
│    1. Filter evidence context by domain       │
│    2. Build system prompt + user prompt       │
│    3. Call LLM (with retry x2, fallback mock) │
│    4. Normalize response (fix enums/types)    │
│    5. Validate via Pydantic schema            │
│    6. Update Board Context                    │
└───────────┬─────────────────────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  POST /api/boardroom/consensus│
│  Consensus Engine:           │
│    - Count positions         │
│    - Apply decision rules    │
│    - Detect conflicts        │
│    - Aggregate risks/actions │
│    - Build executive summary │
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  Report Generation           │
│  - Structured JSON report    │
│  - PDF rendering (fpdf2)     │
│  - Persist to PostgreSQL     │
└─────────────────────────────┘
```

---

### 3. Reusable Components

| Component | Location | Reusability |
|-----------|----------|-------------|
| `retry_llm_call()` | `agents/retry.py` | Used by ALL agents — fully generic |
| `normalize_agent_response()` | `agents/response_normalizer.py` | Handles any agent schema quirks |
| `format_prompt_with_evidence()` | `agents/evidence.py` | Shared prompt builder |
| `extract_evidence_facts()` | `agents/evidence_extractor.py` | Mock response evidence |
| `build_evidence_rationale_prefix()` | `agents/evidence_extractor.py` | Department-specific evidence prefix |
| `BaseLLMProvider` | `agents/llm_provider.py` | Abstract LLM interface |
| `get_provider()` | `agents/llm_provider.py` | Factory for LLM backends |
| `MCPRegistry` | `mcp/registry.py` | Central tool access with usage tracking |
| `summarize_mcp_data()` | `mcp/summarizer.py` | Data → structured evidence text |
| `ConsensusEngineService` | `consensus/service.py` | Works with any agent count |
| `ReportGeneratorService` | `reports/service.py` | Generic report from Board Context |
| `BoardContextService` | `board_context/service.py` | Generic session management |
| `StorageService` | `mcp_hub/storage_service.py` | PostgreSQL persistence layer |

---

### 4. Hardcoded Assumptions Limiting Expansion

| Issue | Location | Impact |
|-------|----------|--------|
| **Explicit agent imports** | `orchestrator/service.py` | Every new agent requires adding imports + dict entry |
| **Stale agent list** | `routes/agents.py` | Only lists 8 agents (finance→CDO), 12 new agents missing |
| **Explicit workspace routes** | `routes/workspace.py` | One endpoint per agent — hardcoded for 8 agents only |
| **Category mapping only references 8 agents** | `decision_router/labels.py` | CATEGORY_AGENT_MAPPING never routes to new 12 agents |
| **Domain keywords duplicated** | `orchestrator/service.py` | DOMAIN_EVIDENCE_KEYWORDS repeated from router — inconsistency risk |
| **LLM semaphore = 2** | `agents/llm_provider.py` | 20 agents sharing 2 concurrent slots = 50s+ per wave |
| **WAVE_SIZE = 4 hardcoded** | `orchestrator/service.py` | Not adaptive to agent count or API limits |
| **Evidence extractor only handles 8 departments** | `agents/evidence_extractor.py` | `build_evidence_rationale_prefix()` has if/elif for 8 depts only |
| **Training data = 10 samples/category** | `decision_router/dataset.py` | Insufficient for 20-agent routing accuracy |

---

### 5. Code Duplication

| Duplication | Where | Fix |
|-------------|-------|-----|
| Agent service boilerplate | Every `service.py` copies same pattern | Extract `BaseAgentService` class |
| Domain keyword lists | Orchestrator + Decision Router both define domain keywords | Single source of truth |
| Position/confidence mock logic | Every mock response repeats keyword→position logic | Shared mock strategy helper |
| Parse-and-validate pattern | Every service has identical JSON parsing logic | Shared `parse_llm_json(agent_id, raw)` |
| Evidence prefix logic | Only covers 8 departments in evidence_extractor | Make it data-driven via config |
| Error handling in workspace routes | 8 identical try/except blocks | Generic workspace endpoint |

---

### 6. Scalability Bottlenecks

1. **LLM Concurrency**: `asyncio.Semaphore(2)` — With 20 agents, only 2 can call LLM simultaneously. 5 waves × 5s = 25s minimum latency just from delays.

2. **In-Memory Sessions**: Single-process `dict` with 200 max sessions. No horizontal scaling. No persistence of in-flight sessions.

3. **Wave Scheduling**: Fixed WAVE_SIZE=4 regardless of actual API capacity. 20 agents = 5 waves = 20+ seconds of mandatory delays.

4. **Training Data**: Only 140 samples for 14 categories. Adding new categories for 12 new agent domains not reflected.

5. **Single LLM Provider Instance**: All agents share one GroqProvider. No per-agent rate tracking or priority.

6. **Report PDF Generation**: Synchronous fpdf2 rendering in API thread. Large reports could block.

7. **Evidence Filtering**: O(n×m) keyword matching per evidence line per agent. Crude but acceptable for current scale.

---

### 7. Architectural Improvements Before Adding More Agents

#### Priority 1: Dynamic Agent Registry
```python
# Replace hardcoded imports with dynamic loading
class AgentRegistry:
    _agents: dict[str, tuple[type, type]] = {}
    
    @classmethod
    def register(cls, agent_id: str, service_cls, request_cls):
        cls._agents[agent_id] = (service_cls, request_cls)
    
    @classmethod
    def get(cls, agent_id: str):
        return cls._agents.get(agent_id)
```

#### Priority 2: Update Decision Router
- Add new 12 agents to `CATEGORY_AGENT_MAPPING`
- Add domain-specific training data for new categories
- Add new `DOMAIN_SIGNALS` for keyword expansion

#### Priority 3: Increase LLM Concurrency
- Change `LLM_MAX_CONCURRENT` default from 2 to 4-6
- Consider per-agent rate limiting vs global semaphore

#### Priority 4: Generic Workspace Endpoint
- Replace 8 explicit endpoints with: `POST /api/workspace/{agent_id}`
- Dynamic service lookup from registry

#### Priority 5: Update Agent List Route
- `routes/agents.py` should return all 20 agents from registry

#### Priority 6: Update Evidence Extractor
- Make `build_evidence_rationale_prefix()` data-driven
- Use a template dict instead of if/elif chain

---

## PHASE 2: NEW AGENT SPECIFICATIONS

> Note: All 12 agents are already implemented in the codebase at `backend/app/agents/`.
> Below are the complete specifications for each.

---

### Agent 1: CEO Agent

| Field | Value |
|-------|-------|
| **agent_id** | `ceo` |
| **Title** | Chief Executive Officer |
| **Short** | CEO |
| **Executive Role** | Sets corporate vision, makes final resource allocation decisions, aligns stakeholders |
| **Department Objective** | Maximize long-term shareholder value through strategic direction and organizational alignment |
| **Decision Boundaries** | Strategic direction only — does NOT do financial modeling (CFO), technology choices (CTO), legal review (GC) |
| **Domain Expertise** | Corporate strategy, stakeholder management, competitive positioning, executive prioritization, M&A direction |

**Input Schema**: `{ scenario: str (min 20 chars), context: Optional[str] }`

**Output Schema**:
```json
{
  "agent_id": "ceo",
  "round": 1,
  "position": "support|oppose|neutral|conditional",
  "confidence": 0.0-1.0,
  "domain_assessment": {
    "strategic_alignment": "How proposal aligns with company vision",
    "stakeholder_impact": "Impact on key stakeholders",
    "competitive_positioning": "Market position effect",
    "execution_priority": "Urgency and resource priority",
    "risk_level": "low|medium|high"
  },
  "summary": "One-sentence position statement",
  "rationale": "2-4 paragraphs of strategic reasoning",
  "risks": ["Specific strategic risks"],
  "conditions": ["Measurable conditions for support"],
  "metrics_to_track": ["Strategic KPIs"]
}
```

**Position Logic**: support if strategy-aligned + competitive advantage; oppose if misaligned; conditional if promising but needs validation

**Confidence Calculation**: Based on strategic clarity (evidence of market data, competitive intel, stakeholder alignment)

---

### Agent 2: Chief Information Security Officer (CISO)

| Field | Value |
|-------|-------|
| **agent_id** | `ciso` |
| **Title** | Chief Information Security Officer |
| **Short** | CISO |
| **Executive Role** | Protects organization's information assets, manages cyber risk, ensures security compliance |
| **Department Objective** | Minimize security risk exposure while enabling business operations |
| **Decision Boundaries** | Security risk ONLY — not financial ROI (CFO), not legal contracts (GC), not IT architecture (CTO) |
| **Domain Expertise** | Threat assessment, vulnerability analysis, security architecture, data protection, SOC2/ISO27001/NIST, incident response, access control |

**Domain Assessment Schema**:
```json
{
  "threat_exposure": "New attack surface or threats introduced",
  "data_protection_impact": "Impact on sensitive data handling",
  "compliance_posture": "Security compliance status (SOC2, ISO27001)",
  "security_investment": "Security controls and costs needed",
  "security_risk": "low|medium|high|critical"
}
```

**Risk Categories**: Threat surface expansion, data breach potential, compliance gap creation, vendor security risk, insider threat amplification

---

### Agent 3: Chief Risk Officer

| Field | Value |
|-------|-------|
| **agent_id** | `risk` |
| **Title** | Chief Risk Officer |
| **Short** | CRO-Risk |
| **Executive Role** | Quantifies and manages enterprise-wide risk, aligns decisions with risk appetite |
| **Department Objective** | Ensure decisions remain within organizational risk tolerance while maximizing risk-adjusted returns |
| **Decision Boundaries** | Enterprise risk quantification ONLY — not financial returns (CFO), not security specifics (CISO), not legal liability (GC) |
| **Domain Expertise** | Risk identification, probability assessment, impact quantification, Monte Carlo analysis, risk appetite alignment, scenario planning |

**Domain Assessment Schema**:
```json
{
  "risk_exposure": "Quantified risk exposure (probability × impact)",
  "probability_assessment": "Likelihood of adverse outcomes",
  "mitigation_strategy": "Risk mitigation recommendations",
  "residual_risk": "Remaining risk after controls",
  "risk_level": "low|medium|high|critical"
}
```

**Risk Categories**: Operational risk, strategic risk, execution risk, market risk, concentration risk, reputational risk

---

### Agent 4: Compliance Officer

| Field | Value |
|-------|-------|
| **agent_id** | `compliance` |
| **Title** | Chief Compliance Officer |
| **Short** | CCO |
| **Executive Role** | Ensures regulatory compliance, maintains governance frameworks, manages audit readiness |
| **Department Objective** | Achieve and maintain compliance with all applicable regulations while enabling business innovation |
| **Decision Boundaries** | Regulatory compliance ONLY — not security implementation (CISO), not legal strategy (GC), not financial impact (CFO) |
| **Domain Expertise** | GDPR, SOX, HIPAA, PCI-DSS, regulatory mapping, policy gaps, governance frameworks, audit preparation, third-party compliance |

**Domain Assessment Schema**:
```json
{
  "regulatory_impact": "Regulations affected by this proposal",
  "compliance_gaps": "Identified compliance gaps",
  "remediation_effort": "Effort to achieve compliance",
  "audit_readiness": "Impact on audit posture",
  "compliance_status": "compliant|non_compliant|requires_review"
}
```

---

### Agent 5: Chief Strategy Officer

| Field | Value |
|-------|-------|
| **agent_id** | `strategy` |
| **Title** | Chief Strategy Officer |
| **Short** | CSO |
| **Executive Role** | Drives corporate strategy, competitive analysis, and long-term planning |
| **Department Objective** | Position the company for sustainable competitive advantage through data-driven strategic decisions |
| **Decision Boundaries** | Strategic analysis ONLY — not financial modeling (CFO), not technology choices (CTO), not operational execution (COO) |
| **Domain Expertise** | Competitive landscape, market dynamics, TAM/SAM/SOM, portfolio strategy, M&A rationale, first-mover analysis, moat assessment |

**Domain Assessment Schema**:
```json
{
  "market_opportunity": "Addressable market and growth potential",
  "competitive_advantage": "Differentiation and moat analysis",
  "strategic_fit": "Alignment with current strategic plan",
  "execution_complexity": "Strategic execution difficulty",
  "strategic_priority": "low|medium|high|critical"
}
```

---

### Agent 6: Product Management Officer

| Field | Value |
|-------|-------|
| **agent_id** | `product` |
| **Title** | Chief Product Officer |
| **Short** | CPO |
| **Executive Role** | Owns product strategy, roadmap prioritization, and product-market fit validation |
| **Department Objective** | Build products users love that generate sustainable revenue growth |
| **Decision Boundaries** | Product strategy ONLY — not engineering (CTO), not pricing (CFO), not campaigns (CMO) |
| **Domain Expertise** | Product-market fit, user needs, roadmap alignment, MVP definition, NPS/retention/adoption, competitive product analysis |

**Domain Assessment Schema**:
```json
{
  "product_market_fit": "Demand validation and user need",
  "roadmap_impact": "Effect on current product roadmap",
  "user_experience": "UX implications and user journey impact",
  "build_vs_buy": "Make/buy/partner analysis",
  "feasibility": "straightforward|moderate|complex|infeasible"
}
```

---

### Agent 7: Customer Success Officer

| Field | Value |
|-------|-------|
| **agent_id** | `customer_success` |
| **Title** | Chief Customer Officer |
| **Short** | CCusO |
| **Executive Role** | Maximizes customer lifetime value through retention, satisfaction, and advocacy |
| **Department Objective** | Reduce churn, increase NPS, and transform customers into advocates |
| **Decision Boundaries** | Customer retention/satisfaction ONLY — not sales pipeline (CRO), not marketing (CMO), not pricing (CFO) |
| **Domain Expertise** | Customer health scores, churn prediction, NPS/CSAT impact, onboarding complexity, support load, customer lifecycle |

**Domain Assessment Schema**:
```json
{
  "customer_impact": "Impact on existing customers",
  "retention_risk": "Churn risk assessment",
  "satisfaction_forecast": "Expected NPS/CSAT effect",
  "support_requirements": "Customer support needs",
  "customer_risk": "low|medium|high"
}
```

---

### Agent 8: Supply Chain Officer

| Field | Value |
|-------|-------|
| **agent_id** | `supply_chain` |
| **Title** | Chief Supply Chain Officer |
| **Short** | CSCO |
| **Executive Role** | Optimizes end-to-end supply chain, manages vendor risk, ensures delivery capability |
| **Department Objective** | Build resilient, cost-effective supply chains that scale with business growth |
| **Decision Boundaries** | Supply chain/logistics ONLY — not financial analysis (CFO), not IT systems (CTO), not contracts (GC) |
| **Domain Expertise** | Supplier diversity, lead times, inventory optimization, logistics costs, procurement strategy, vendor risk, demand forecasting |

**Domain Assessment Schema**:
```json
{
  "supply_chain_impact": "Effect on supply chain operations",
  "vendor_dependency": "Supplier risk and concentration",
  "logistics_complexity": "Distribution and fulfillment challenges",
  "procurement_needs": "Sourcing requirements",
  "operational_risk": "low|medium|high|critical"
}
```

---

### Agent 9: ESG & Sustainability Officer

| Field | Value |
|-------|-------|
| **agent_id** | `esg` |
| **Title** | ESG & Sustainability Officer |
| **Short** | ESG |
| **Executive Role** | Drives environmental, social, and governance strategy; ensures sustainability compliance |
| **Department Objective** | Align business decisions with ESG frameworks while creating measurable positive impact |
| **Decision Boundaries** | ESG/sustainability ONLY — not financial ROI (CFO), not legal specifics (GC), not IT implementation (CTO) |
| **Domain Expertise** | Carbon footprint, emissions targets, ESG scoring, GRI/SASB/TCFD reporting, social impact, DEI, governance transparency |

**Domain Assessment Schema**:
```json
{
  "environmental_impact": "Carbon footprint, resource usage, emissions",
  "social_impact": "Community, diversity, labor practices",
  "governance_implications": "Board oversight, transparency, ethics",
  "sustainability_score": "Alignment with ESG frameworks (GRI, SASB, TCFD)",
  "esg_risk": "low|medium|high|critical"
}
```

---

### Agent 10: AI Governance & Ethics Officer

| Field | Value |
|-------|-------|
| **agent_id** | `ai_governance` |
| **Title** | AI Governance & Ethics Officer |
| **Short** | AIGO |
| **Executive Role** | Ensures responsible AI deployment, manages algorithmic fairness, oversees model governance |
| **Department Objective** | Enable AI innovation while preventing harm, bias, and ethical violations |
| **Decision Boundaries** | AI ethics/governance ONLY — not AI architecture (CTO), not data engineering (CDO), not legal specifics (GC) |
| **Domain Expertise** | Algorithmic bias, model explainability, EU AI Act, NIST AI RMF, data ethics, automated decision impact |

**Domain Assessment Schema**:
```json
{
  "ethical_risk": "Bias, fairness, discrimination concerns",
  "transparency_requirements": "Explainability and interpretability needs",
  "governance_framework": "AI governance policies and oversight",
  "societal_impact": "Broader societal implications",
  "ai_risk_level": "low|medium|high|critical"
}
```

---

### Agent 11: Innovation & Research Officer

| Field | Value |
|-------|-------|
| **agent_id** | `innovation` |
| **Title** | Chief Innovation Officer |
| **Short** | CIO-Inn |
| **Executive Role** | Drives R&D strategy, evaluates emerging technologies, manages innovation pipeline |
| **Department Objective** | Maintain technological edge through strategic research and breakthrough innovation |
| **Decision Boundaries** | Innovation/R&D ONLY — not production engineering (CTO), not financial modeling (CFO), not market positioning (CMO) |
| **Domain Expertise** | Technology readiness levels, R&D investment, patent landscape, emerging tech radar, proof-of-concept design, innovation portfolio |

**Domain Assessment Schema**:
```json
{
  "innovation_potential": "Novelty and breakthrough potential",
  "technology_readiness": "TRL level and maturity assessment",
  "research_requirements": "R&D investment and timeline",
  "ip_opportunity": "Intellectual property and patent potential",
  "innovation_risk": "low|medium|high"
}
```

---

### Agent 12: Investor Relations Officer

| Field | Value |
|-------|-------|
| **agent_id** | `investor_relations` |
| **Title** | Investor Relations Officer |
| **Short** | IRO |
| **Executive Role** | Manages investor communication, shapes market perception, advises on earnings impact |
| **Department Objective** | Maximize shareholder confidence through transparent communication and strategic positioning |
| **Decision Boundaries** | Investor communication ONLY — not internal finance (CFO), not legal filings (GC), not product strategy (CPO) |
| **Domain Expertise** | Analyst sentiment, earnings guidance, shareholder value messaging, SEC implications, market cap impact, dividend considerations |

**Domain Assessment Schema**:
```json
{
  "market_perception": "How investors/analysts will perceive this",
  "earnings_impact": "Effect on EPS, guidance, quarterly results",
  "shareholder_value": "Long-term shareholder value creation",
  "communication_strategy": "Messaging to investor community",
  "investor_sentiment": "positive|neutral|negative|mixed"
}
```

---

## PHASE 3: LIVE KNOWLEDGE ARCHITECTURE (RAG LAYER DESIGN)

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    RETRIEVAL-AUGMENTED GENERATION                │
│                                                                  │
│  Business Proposal                                               │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ Source Planner   │  Determines which connectors to invoke     │
│  │ (per agent)      │  based on agent domain + scenario keywords │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────────────────────────────────┐                │
│  │        CONNECTOR FRAMEWORK                    │                │
│  │                                               │                │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │                │
│  │  │ SQL      │ │ REST API │ │ Vector DB│     │                │
│  │  │ Connector│ │ Connector│ │ Connector│     │                │
│  │  └──────────┘ └──────────┘ └──────────┘     │                │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐     │                │
│  │  │ File     │ │ Finance  │ │ News     │     │                │
│  │  │ Connector│ │ API      │ │ API      │     │                │
│  │  └──────────┘ └──────────┘ └──────────┘     │                │
│  └────────────────────┬────────────────────────┘                │
│                       │                                          │
│                       ▼                                          │
│  ┌─────────────────────────────────────────────┐                │
│  │  EVIDENCE RANKER                              │                │
│  │  - Relevance scoring                          │                │
│  │  - Freshness weighting                        │                │
│  │  - Source credibility                         │                │
│  │  - Domain filtering                           │                │
│  │  - Token budget allocation                    │                │
│  └────────────────────┬────────────────────────┘                │
│                       │                                          │
│                       ▼                                          │
│  ┌─────────────────────────────────────────────┐                │
│  │  CONTEXT BUILDER                              │                │
│  │  - Format evidence for prompt injection       │                │
│  │  - Source attribution tags                    │                │
│  │  - Confidence scores per source               │                │
│  │  - Truncation to token limits                 │                │
│  └────────────────────┬────────────────────────┘                │
│                       │                                          │
│                       ▼                                          │
│  ┌─────────────────────────────────────────────┐                │
│  │  LLM INVOCATION                               │                │
│  │  System prompt + scenario + ranked evidence   │                │
│  │  → Structured JSON response with citations    │                │
│  └─────────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### Agent-to-Source Mapping

| Agent | Primary Sources | Data Types |
|-------|----------------|------------|
| CFO (finance) | ERP, Balance sheets, Yahoo Finance, Alpha Vantage | Financial statements, stock prices, revenue data |
| CMO (marketing) | Google Trends, CRM, Social analytics | Market trends, customer segments, campaign data |
| CTO (it) | GitHub, Jira, Cloud monitoring, Datadog | System metrics, issue tracking, deployment stats |
| GC (legal) | Regulatory databases, GDPR portals, Case law | Regulations, compliance requirements, court rulings |
| CISO | NVD/CVE feeds, Threat intel, NIST | Vulnerability data, threat assessments, security advisories |
| CRO-Risk | Monte Carlo engines, Risk databases | Risk registers, probability distributions, loss data |
| CCO (compliance) | Regulatory APIs, Audit databases | Compliance status, policy documents, audit findings |
| CSO (strategy) | Market research, Competitive intel | Industry reports, competitor analysis, market sizing |
| CPO (product) | Product analytics, User research | Usage metrics, feature requests, NPS data |
| CCusO (customer_success) | Zendesk, Salesforce, CSAT tools | Ticket data, health scores, churn indicators |
| CSCO (supply_chain) | SAP, Inventory systems, Logistics | Inventory levels, lead times, vendor data |
| ESG | ESG databases, Carbon calculators | Emissions data, ESG scores, sustainability reports |
| AIGO (ai_governance) | Model registries, Bias testing tools | Model cards, fairness metrics, audit logs |
| CIO-Inn (innovation) | Patent databases, Research papers | Patent landscape, technology trends, R&D data |
| IRO (investor_relations) | SEC filings, Market news, Analyst reports | Earnings data, analyst estimates, shareholder info |

### Domain Isolation Rules

Each agent's retrieval layer MUST:
1. Only access sources mapped to its domain
2. Never retrieve data belonging to another department
3. Tag all evidence with source, timestamp, and confidence
4. Respect token budgets (max 1500 chars evidence per agent)
5. Cache frequently-accessed data (5-minute TTL for APIs)
6. Degrade gracefully if a source is unavailable (mark as "missing data")

### Modular Connector Framework Design

```python
# Base connector interface
class BaseConnector(ABC):
    """Every data source connector implements this interface."""
    
    connector_id: str           # Unique identifier
    connector_type: str         # sql, rest_api, vector_db, file, finance_api, news_api
    domains: list[str]          # Which agents can use this connector
    
    @abstractmethod
    async def connect(self) -> None: ...
    
    @abstractmethod
    async def retrieve(self, query: RetrievalQuery) -> list[Evidence]: ...
    
    @abstractmethod
    async def health_check(self) -> bool: ...

# Every connector includes:
class ConnectorConfig:
    authentication: AuthConfig       # API keys, tokens, credentials
    retry_policy: RetryConfig        # max_retries, backoff strategy
    timeout: TimeoutConfig           # connect_timeout, read_timeout
    rate_limit: RateLimitConfig      # requests/second, burst limit
    cache: CacheConfig               # TTL, max entries, invalidation
    logging: LogConfig               # log level, structured logging
    error_handling: ErrorConfig      # fallback behavior, circuit breaker
    async_execution: bool = True     # Always async by default
```

### Supported Connectors (Phase 4 Implementation)

| Category | Connectors | Priority |
|----------|-----------|----------|
| **SQL Databases** | PostgreSQL, MySQL, Snowflake, Databricks | High |
| **CRM/Business** | Salesforce, HubSpot, SAP | High |
| **DevOps** | Jira, GitHub, Datadog, Prometheus | Medium |
| **Finance APIs** | Alpha Vantage, Yahoo Finance, Polygon.io | High |
| **News/Trends** | NewsAPI, Google Trends, RSS feeds | Medium |
| **Government** | Government regulatory APIs, SEC EDGAR | Medium |
| **Vector Databases** | FAISS, ChromaDB, Pinecone | High |
| **Internal** | Internal REST APIs, Custom connectors | Medium |

### Evidence Schema (returned by all connectors)

```python
class Evidence(BaseModel):
    source_id: str              # Connector that produced this
    source_type: str            # sql, api, vector, file
    domain: str                 # finance, legal, security, etc.
    content: str                # The actual evidence text
    relevance_score: float      # 0.0-1.0 computed relevance
    freshness: datetime         # When the data was generated/fetched
    confidence: float           # Source reliability (0.0-1.0)
    citation: str               # Human-readable source citation
    metadata: dict              # Source-specific metadata
```

---

## PHASE 4: IMPLEMENTATION PLAN

---

### Complete Roadmap (Ordered)

#### Step 1: Fix Existing Integration Issues (Day 1)
- Update `routes/agents.py` to list all 20 agents
- Update `routes/workspace.py` to add endpoints for 12 new agents (or make generic)
- Update `decision_router/labels.py` CATEGORY_AGENT_MAPPING to include new agents
- Update `decision_router/service.py` DOMAIN_SIGNALS to include new agents
- Update `evidence_extractor.py` `build_evidence_rationale_prefix()` for new departments
- Verify orchestrator already imports all 20 agents ✓ (confirmed in service.py)

#### Step 2: Decision Router Enhancement (Day 2)
- Add new training data to `dataset.py` for new agent domains
- Add new categories if needed (e.g., `cybersecurity`, `innovation`, `sustainability`)
- Retrain model with expanded dataset
- Test routing accuracy with new agent coverage

#### Step 3: Retrieval Layer Foundation (Days 3-4)
- Create `backend/app/retrieval/` module:
  - `__init__.py`
  - `base_connector.py` — Abstract BaseConnector class
  - `connector_config.py` — Configuration models
  - `evidence.py` — Evidence schema + ranking
  - `source_planner.py` — Domain → connector mapping
  - `context_builder.py` — Evidence → prompt injection
  - `registry.py` — Connector registry (lazy loading)
  - `cache.py` — Shared caching layer (TTL-based)

#### Step 4: Core Connectors (Days 5-8)
- `retrieval/connectors/sql_connector.py` — PostgreSQL, MySQL, Snowflake
- `retrieval/connectors/rest_api_connector.py` — Generic REST with auth
- `retrieval/connectors/vector_db_connector.py` — FAISS, ChromaDB
- `retrieval/connectors/file_connector.py` — PDF, Excel, CSV (upgrade from existing MCP)
- `retrieval/connectors/finance_api_connector.py` — Alpha Vantage, Yahoo Finance, Polygon.io
- `retrieval/connectors/news_connector.py` — NewsAPI, RSS, Google Trends
- `retrieval/connectors/government_connector.py` — SEC EDGAR, regulatory APIs
- `retrieval/connectors/devops_connector.py` — Jira, GitHub, Datadog

#### Step 5: Agent Integration with RAG (Days 9-10)
- Add `retrieval_sources` config to each agent module
- Modify `service.py` pattern to call retrieval before LLM
- Update `evidence.py` to accept structured Evidence objects
- Add source attribution to agent responses

#### Step 6: Performance & Scaling (Day 11)
- Increase `LLM_MAX_CONCURRENT` default to 4
- Make `WAVE_SIZE` configurable via env var
- Add per-agent timeout configurability
- Add retrieval timeout (5s max, fail open)

#### Step 7: Testing & Documentation (Day 12)
- Unit tests for each new connector
- Integration tests for full RAG pipeline
- Update API documentation
- Architecture diagrams (Mermaid)

---

### Required New Folders

```
backend/app/retrieval/
├── __init__.py
├── base_connector.py
├── connector_config.py
├── evidence.py
├── source_planner.py
├── context_builder.py
├── registry.py
├── cache.py
└── connectors/
    ├── __init__.py
    ├── sql_connector.py
    ├── rest_api_connector.py
    ├── vector_db_connector.py
    ├── file_connector.py
    ├── finance_api_connector.py
    ├── news_connector.py
    ├── government_connector.py
    └── devops_connector.py
```

### Required New Models

| Model | Location | Purpose |
|-------|----------|---------|
| `Evidence` | `retrieval/evidence.py` | Standardized evidence from any source |
| `RetrievalQuery` | `retrieval/evidence.py` | Query request for connectors |
| `ConnectorConfig` | `retrieval/connector_config.py` | Auth + retry + cache config |
| `SourcePlan` | `retrieval/source_planner.py` | Which connectors to invoke |
| `RankedEvidence` | `retrieval/evidence.py` | Scored and sorted evidence set |

### Required Services

| Service | Location | Purpose |
|---------|----------|---------|
| `RetrievalService` | `retrieval/__init__.py` | Orchestrate retrieval for an agent |
| `EvidenceRanker` | `retrieval/evidence.py` | Score and rank evidence |
| `SourcePlanner` | `retrieval/source_planner.py` | Map agent domain → connectors |
| `ConnectorRegistry` | `retrieval/registry.py` | Register and lookup connectors |
| `CacheService` | `retrieval/cache.py` | Shared TTL cache |

### Required APIs

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/retrieval/connectors` | GET | List registered connectors |
| `/api/retrieval/connectors/{id}/health` | GET | Health check a connector |
| `/api/retrieval/evidence/{agent_id}` | GET | Get live evidence for agent |
| `/api/workspace/{agent_id}` | POST | Generic single-agent endpoint (replaces 8 specific) |

### Required Connector Configurations

Each connector requires environment variables:
```env
# SQL Connectors
POSTGRES_URL=postgresql://...
MYSQL_URL=mysql://...
SNOWFLAKE_URL=snowflake://...

# Finance APIs
ALPHA_VANTAGE_API_KEY=...
POLYGON_API_KEY=...

# News APIs  
NEWS_API_KEY=...

# DevOps
JIRA_URL=...
JIRA_TOKEN=...
GITHUB_TOKEN=...
DATADOG_API_KEY=...

# Vector DB
CHROMA_URL=...
FAISS_INDEX_PATH=...

# CRM
SALESFORCE_CLIENT_ID=...
HUBSPOT_API_KEY=...
```

### Required Database Changes

1. Add `evidence` table (already exists in models.py ✓)
2. Add `connector_configs` table for dynamic connector management
3. Add `retrieval_logs` table for tracking connector usage and performance

### Required Tests

| Test File | Coverage |
|-----------|----------|
| `tests/test_retrieval_base.py` | BaseConnector interface tests |
| `tests/test_connectors_sql.py` | SQL connector with mock DB |
| `tests/test_connectors_api.py` | REST/Finance/News API connectors |
| `tests/test_source_planner.py` | Domain → connector mapping |
| `tests/test_evidence_ranker.py` | Relevance scoring logic |
| `tests/test_context_builder.py` | Evidence → prompt formatting |
| `tests/test_new_agents.py` | All 12 new agents mock responses |
| `tests/test_integration_rag.py` | Full pipeline integration |
| `tests/test_router_expanded.py` | Updated decision router accuracy |

### Estimated Implementation Order

| Priority | Task | Effort | Dependencies |
|----------|------|--------|--------------|
| 1 | Fix integration issues (routes, router, labels) | 2 hours | None |
| 2 | Create retrieval framework base | 4 hours | None |
| 3 | Implement SQL connector | 3 hours | Step 2 |
| 4 | Implement Finance API connectors | 3 hours | Step 2 |
| 5 | Implement REST/News connectors | 3 hours | Step 2 |
| 6 | Implement Vector DB connector | 3 hours | Step 2 |
| 7 | Evidence ranker + context builder | 3 hours | Steps 3-6 |
| 8 | Source planner per agent | 2 hours | Step 7 |
| 9 | Integrate RAG into agent services | 4 hours | Step 8 |
| 10 | Performance tuning | 2 hours | Step 9 |
| 11 | Tests + documentation | 4 hours | All above |

**Total estimated effort: ~33 hours**

---

## CURRENT STATUS

- ✅ All 12 new agents are ALREADY IMPLEMENTED in the codebase
- ✅ Orchestrator already imports and coordinates all 20 agents
- ✅ Evidence keywords for all 20 agents defined in orchestrator
- ⚠️ `routes/agents.py` only lists original 8 (needs update)
- ⚠️ `routes/workspace.py` only has endpoints for original 8 (needs update)
- ⚠️ `decision_router/labels.py` CATEGORY_AGENT_MAPPING only maps to original 8 (needs update)
- ❌ RAG/Retrieval layer not yet implemented (Phase 3-4 pending)
- ❌ No live data connectors (all evidence comes from file uploads via MCP)

---

## AWAITING YOUR APPROVAL

No code changes have been made. This document contains:
1. ✅ Complete architecture audit
2. ✅ Full specifications for all 12 new agents
3. ✅ RAG layer design
4. ✅ Connector framework architecture
5. ✅ Implementation roadmap

**Ready to proceed with implementation upon your approval.**
