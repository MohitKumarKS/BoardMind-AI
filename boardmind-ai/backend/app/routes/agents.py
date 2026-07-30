"""Agent listing API routes.

Provides the endpoint to list all available department agents.
Updated to include all 20 executive agents.
"""

from fastapi import APIRouter

router = APIRouter()


# Complete registry of all 20 executive agents
ALL_AGENTS = [
    {"agent_id": "finance", "title": "Chief Financial Officer", "short": "CFO"},
    {"agent_id": "marketing", "title": "Chief Marketing Officer", "short": "CMO"},
    {"agent_id": "sales", "title": "Chief Revenue Officer", "short": "CRO"},
    {"agent_id": "hr", "title": "Chief Human Resources Officer", "short": "CHRO"},
    {"agent_id": "operations", "title": "Chief Operating Officer", "short": "COO"},
    {"agent_id": "legal", "title": "General Counsel", "short": "GC"},
    {"agent_id": "it", "title": "Chief Technology Officer", "short": "CTO"},
    {"agent_id": "business_analytics", "title": "Chief Data Officer", "short": "CDO"},
    {"agent_id": "ceo", "title": "Chief Executive Officer", "short": "CEO"},
    {"agent_id": "ciso", "title": "Chief Information Security Officer", "short": "CISO"},
    {"agent_id": "risk", "title": "Chief Risk Officer", "short": "CRO-Risk"},
    {"agent_id": "compliance", "title": "Chief Compliance Officer", "short": "CCO"},
    {"agent_id": "strategy", "title": "Chief Strategy Officer", "short": "CSO"},
    {"agent_id": "product", "title": "Chief Product Officer", "short": "CPO"},
    {"agent_id": "customer_success", "title": "Chief Customer Officer", "short": "CCusO"},
    {"agent_id": "supply_chain", "title": "Chief Supply Chain Officer", "short": "CSCO"},
    {"agent_id": "esg", "title": "ESG & Sustainability Officer", "short": "ESG"},
    {"agent_id": "ai_governance", "title": "AI Governance & Ethics Officer", "short": "AIGO"},
    {"agent_id": "innovation", "title": "Chief Innovation Officer", "short": "CIO-Inn"},
    {"agent_id": "investor_relations", "title": "Investor Relations Officer", "short": "IRO"},
]


@router.get("/")
def list_agents():
    """List all available department agents."""
    return ALL_AGENTS


@router.get("/{agent_id}")
def get_agent(agent_id: str):
    """Get details for a specific agent."""
    for agent in ALL_AGENTS:
        if agent["agent_id"] == agent_id:
            return agent
    return {"agent_id": agent_id, "status": "not_found"}
