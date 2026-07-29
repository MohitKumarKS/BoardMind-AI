"""Database engine and session management for MCP Knowledge Hub."""

import logging
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .config import get_database_url, is_hub_configured
from .models import Base

logger = logging.getLogger(__name__)

_engine = None
_session_factory: Optional[async_sessionmaker] = None


async def init_database() -> bool:
    """Initialize the database connection and create tables.

    Returns True if successful, False if database is unavailable.
    """
    global _engine, _session_factory

    if not is_hub_configured():
        logger.info("MCP Knowledge Hub: No database URL configured — running without persistence")
        return False

    try:
        url = get_database_url()
        _engine = create_async_engine(url, echo=False, pool_size=5, max_overflow=10)

        # Create tables if they don't exist
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        _session_factory = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
        logger.info("MCP Knowledge Hub: Database initialized successfully")
        return True

    except Exception as e:
        logger.warning(f"MCP Knowledge Hub: Database initialization failed — {e}")
        _engine = None
        _session_factory = None
        return False


def get_session() -> Optional[AsyncSession]:
    """Get a database session. Returns None if database is not available."""
    if _session_factory is None:
        return None
    return _session_factory()


def is_database_ready() -> bool:
    """Check if database is initialized and ready."""
    return _session_factory is not None
