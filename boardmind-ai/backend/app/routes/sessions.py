from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_sessions():
    """List all deliberation sessions."""
    return []


@router.post("/")
def create_session():
    """Create a new deliberation session."""
    return {"message": "Not implemented"}


@router.get("/{session_id}")
def get_session(session_id: str):
    """Get a specific session by ID."""
    return {"session_id": session_id, "status": "not_implemented"}
