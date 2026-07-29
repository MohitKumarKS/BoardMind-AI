"""Evidence Retrieval Service.

Retrieves domain-specific evidence for executive agents.
Supports multiple data sources through a pluggable interface.

Current sources:
- PostgreSQL (stored evidence)
- CSV files (via existing MCP tools)
- REST APIs (future)

Each agent receives only evidence matching its domain.
"""

import logging
from typing import Any, Optional

from sqlalchemy import select

from .database import get_session, is_database_ready
from .models import Evidence

logger = logging.getLogger(__name__)

# Domain keywords for evidence matching
DOMAIN_CATEGORIES: dict[str, list[str]] = {
    "finance": ["finance", "revenue", "cost", "budget", "roi", "investment", "cash_flow", "profit"],
    "marketing": ["marketing", "customer", "brand", "market", "campaign", "acquisition", "positioning"],
    "sales": ["sales", "pipeline", "revenue", "deal", "customer", "demand", "quota"],
    "hr": ["hr", "hiring", "employee", "talent", "workforce", "culture", "training"],
    "operations": ["operations", "supply_chain", "logistics", "capacity", "process", "delivery"],
    "legal": ["legal", "compliance", "regulation", "contract", "privacy", "governance", "ip"],
    "it": ["it", "technology", "security", "infrastructure", "cloud", "architecture", "platform"],
    "business_analytics": ["analytics", "data", "metrics", "kpi", "benchmark", "forecast", "measurement"],
}


class EvidenceService:
    """Retrieves domain-specific evidence for executive agents.

    Queries PostgreSQL for stored evidence matching the agent's domain.
    Falls back gracefully if the database is unavailable.
    """

    async def get_evidence_for_agent(
        self,
        agent_id: str,
        meeting_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Retrieve evidence relevant to a specific agent's domain.

        Args:
            agent_id: The department agent identifier.
            meeting_id: Optional meeting to scope evidence to.
            limit: Maximum evidence items to return.

        Returns:
            List of evidence dicts with source, category, content, metadata.
            Returns empty list if database is unavailable.
        """
        if not is_database_ready():
            return []

        categories = DOMAIN_CATEGORIES.get(agent_id, [agent_id])

        session = get_session()
        if not session:
            return []

        try:
            async with session:
                query = (
                    select(Evidence)
                    .where(Evidence.category.in_(categories))
                    .order_by(Evidence.created_at.desc())
                    .limit(limit)
                )

                if meeting_id:
                    query = query.where(
                        (Evidence.meeting_id == meeting_id) | (Evidence.meeting_id.is_(None))
                    )

                result = await session.execute(query)
                rows = result.scalars().all()

                return [
                    {
                        "id": row.id,
                        "source": row.source,
                        "category": row.category,
                        "content": row.content,
                        "metadata": row.extra_metadata,
                        "created_at": row.created_at.isoformat() if row.created_at else None,
                    }
                    for row in rows
                ]

        except Exception as e:
            logger.error(f"Evidence retrieval failed for agent '{agent_id}': {e}")
            return []

    async def store_evidence(
        self,
        source: str,
        category: str,
        content: str,
        metadata: Optional[dict] = None,
        meeting_id: Optional[str] = None,
    ) -> bool:
        """Store new evidence in the knowledge hub.

        Args:
            source: Origin of the evidence (file, api, database, manual).
            category: Domain category (finance, legal, it, etc.).
            content: The evidence text content.
            metadata: Optional metadata dict.
            meeting_id: Optional meeting association.

        Returns:
            True if stored successfully, False otherwise.
        """
        if not is_database_ready():
            return False

        session = get_session()
        if not session:
            return False

        try:
            async with session:
                evidence = Evidence(
                    source=source,
                    category=category,
                    content=content,
                    extra_metadata=metadata,
                    meeting_id=meeting_id,
                )
                session.add(evidence)
                await session.commit()
                return True

        except Exception as e:
            logger.error(f"Evidence storage failed: {e}")
            return False
