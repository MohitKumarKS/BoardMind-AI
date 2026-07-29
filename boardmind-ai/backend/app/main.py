import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load .env file from the backend directory
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

from app.routes import sessions, agents, reports, workspace, decision_router, boardroom, mcp

app = FastAPI(
    title="BoardMind AI",
    description="Multi-agent decision-making platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workspace.router, prefix="/api/workspace", tags=["workspace"])
app.include_router(boardroom.router, prefix="/api/boardroom", tags=["boardroom"])
app.include_router(decision_router.router, prefix="/api/decision-router", tags=["decision-router"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(mcp.router, prefix="/api/mcp", tags=["mcp"])


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
