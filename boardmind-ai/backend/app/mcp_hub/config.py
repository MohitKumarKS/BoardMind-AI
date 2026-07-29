"""MCP Knowledge Hub configuration."""

import os


def get_database_url() -> str:
    """Get PostgreSQL connection URL from environment."""
    return os.environ.get(
        "MCP_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/boardmind"
    )


def is_hub_configured() -> bool:
    """Check if the MCP Knowledge Hub database is configured."""
    return bool(os.environ.get("MCP_DATABASE_URL"))
