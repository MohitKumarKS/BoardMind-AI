from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_agents():
    """List all available department agents."""
    return [
        {"agent_id": "finance", "title": "Chief Financial Officer", "short": "CFO"},
        {"agent_id": "marketing", "title": "Chief Marketing Officer", "short": "CMO"},
        {"agent_id": "sales", "title": "Chief Revenue Officer", "short": "CRO"},
        {"agent_id": "hr", "title": "Chief Human Resources Officer", "short": "CHRO"},
        {"agent_id": "operations", "title": "Chief Operating Officer", "short": "COO"},
        {"agent_id": "legal", "title": "General Counsel", "short": "GC"},
        {"agent_id": "it", "title": "Chief Technology Officer", "short": "CTO"},
        {"agent_id": "business_analytics", "title": "Chief Data Officer", "short": "CDO"},
    ]


@router.get("/{agent_id}")
def get_agent(agent_id: str):
    """Get details for a specific agent."""
    return {"agent_id": agent_id, "status": "not_implemented"}
