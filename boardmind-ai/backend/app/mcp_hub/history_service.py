"""Historical Intelligence Service.

Retrieves previous board decisions for context.
Supports similarity-based queries using keyword matching.

This is optional — the system works without historical data.
"""

import logging
from typing import Any, Optional

from sqlalchemy import select, or_, func

from .database import get_session, is_database_ready
from .models import Meeting, ExecutiveAnalysis, ConsensusRecord

logger = logging.getLogger(__name__)


class HistoryService:
    """Retrieves historical board decisions for agent context.

    Searches past meetings by keyword similarity and returns
    previous decisions ranked by relevance.
    """

    async def find_similar_meetings(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Find past meetings similar to a given query.

        Uses keyword matching against meeting proposals.
        Returns meetings with their consensus decisions.

        Args:
            query: Search terms or scenario description.
            limit: Maximum results to return.

        Returns:
            List of meeting summaries with decisions.
            Empty list if database unavailable or no matches.
        """
        if not is_database_ready():
            return []

        session = get_session()
        if not session:
            return []

        try:
            # Extract keywords from query for matching
            keywords = self._extract_keywords(query)
            if not keywords:
                return []

            async with session:
                # Search meetings containing any keyword
                filters = [
                    Meeting.proposal.ilike(f"%{kw}%") for kw in keywords[:5]
                ]

                query_stmt = (
                    select(Meeting)
                    .where(or_(*filters))
                    .order_by(Meeting.created_at.desc())
                    .limit(limit)
                )

                result = await session.execute(query_stmt)
                meetings = result.scalars().all()

                summaries = []
                for meeting in meetings:
                    # Get consensus for this meeting
                    consensus_stmt = select(ConsensusRecord).where(
                        ConsensusRecord.meeting_id == meeting.meeting_id
                    )
                    consensus_result = await session.execute(consensus_stmt)
                    consensus = consensus_result.scalar_one_or_none()

                    # Get analyses
                    analyses_stmt = select(ExecutiveAnalysis).where(
                        ExecutiveAnalysis.meeting_id == meeting.meeting_id
                    )
                    analyses_result = await session.execute(analyses_stmt)
                    analyses = analyses_result.scalars().all()

                    summaries.append({
                        "meeting_id": meeting.meeting_id,
                        "proposal_summary": meeting.proposal[:300],
                        "business_category": meeting.business_category,
                        "created_at": meeting.created_at.isoformat() if meeting.created_at else None,
                        "executive_recommendations": [
                            {
                                "role": a.executive_role,
                                "recommendation": a.recommendation,
                                "confidence": a.confidence,
                            }
                            for a in analyses
                        ],
                        "final_decision": consensus.decision if consensus else None,
                        "decision_confidence": consensus.confidence if consensus else None,
                        "consensus_summary": consensus.summary if consensus else None,
                    })

                return summaries

        except Exception as e:
            logger.error(f"Historical query failed: {e}")
            return []

    async def get_meeting_history(
        self, limit: int = 20
    ) -> list[dict[str, Any]]:
        """Get recent meeting history (chronological).

        Returns a simple list of recent meetings with outcomes.
        """
        if not is_database_ready():
            return []

        session = get_session()
        if not session:
            return []

        try:
            async with session:
                query = (
                    select(Meeting)
                    .order_by(Meeting.created_at.desc())
                    .limit(limit)
                )
                result = await session.execute(query)
                meetings = result.scalars().all()

                return [
                    {
                        "meeting_id": m.meeting_id,
                        "title": m.title,
                        "business_category": m.business_category,
                        "created_at": m.created_at.isoformat() if m.created_at else None,
                    }
                    for m in meetings
                ]

        except Exception as e:
            logger.error(f"History retrieval failed: {e}")
            return []

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract meaningful keywords from text for search."""
        # Remove common stop words and short words
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "and",
            "but", "or", "nor", "not", "so", "yet", "both", "either",
            "we", "our", "us", "they", "them", "their", "this", "that",
            "it", "its", "all", "each", "every", "any", "some",
        }

        words = text.lower().split()
        keywords = [
            w.strip(".,;:!?()[]{}\"'")
            for w in words
            if len(w) > 3 and w.lower() not in stop_words
        ]

        # Return unique keywords, prioritizing longer ones
        seen = set()
        unique = []
        for kw in sorted(keywords, key=len, reverse=True):
            if kw not in seen:
                seen.add(kw)
                unique.append(kw)

        return unique[:10]
