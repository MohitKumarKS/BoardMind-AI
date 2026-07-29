"""Web Search MCP Tool.

Provides a search interface for retrieving external information.
Currently returns mock results. Can later connect to a real search
provider (Google, Bing, Tavily, etc.) without changing the interface.
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class WebSearchTool:
    """Searches the web for relevant business information.

    Currently a mock implementation returning structured results.
    Real provider integration can be added without interface changes.
    """

    def search(self, query: str, max_results: int = 5) -> dict[str, Any]:
        """Search for information relevant to a business query.

        Args:
            query: Search query string.
            max_results: Maximum number of results to return.

        Returns:
            Dict with search results, query metadata, and source.
        """
        logger.info(f"Web search (mock): '{query}'")

        results = self._generate_mock_results(query, max_results)

        return {
            "source": "websearch_tool",
            "query": query,
            "result_count": len(results),
            "results": results,
            "provider": "mock",
            "searched_at": datetime.utcnow().isoformat(),
            "note": "Mock results — connect a search provider for real data",
        }

    def _generate_mock_results(self, query: str, max_results: int) -> list[dict[str, str]]:
        """Generate contextually relevant mock search results."""
        query_lower = query.lower()

        # Base results that adapt to query keywords
        mock_results = []

        if any(w in query_lower for w in ["market", "industry", "trend"]):
            mock_results.extend([
                {
                    "title": "Industry Market Analysis Report 2024",
                    "url": "https://example.com/market-analysis-2024",
                    "snippet": "The global market is projected to grow at 12.5% CAGR, reaching $45B by 2027. Key drivers include digital transformation and AI adoption.",
                },
                {
                    "title": "Competitive Landscape Overview",
                    "url": "https://example.com/competitive-landscape",
                    "snippet": "Top 5 players control 62% market share. New entrants have captured 8% in the past 18 months through differentiated offerings.",
                },
            ])

        if any(w in query_lower for w in ["pricing", "cost", "revenue", "financial"]):
            mock_results.extend([
                {
                    "title": "SaaS Pricing Benchmarks 2024",
                    "url": "https://example.com/saas-pricing",
                    "snippet": "Average B2B SaaS ACV is $42K for mid-market. Price increases of 15-25% are common annually. Usage-based models growing 40% YoY.",
                },
                {
                    "title": "Cost Optimization Strategies for Tech Companies",
                    "url": "https://example.com/cost-optimization",
                    "snippet": "Companies achieving 20%+ cost reduction typically focus on cloud optimization (35%), vendor consolidation (25%), and process automation (20%).",
                },
            ])

        if any(w in query_lower for w in ["hiring", "talent", "team", "workforce"]):
            mock_results.extend([
                {
                    "title": "Tech Hiring Trends and Salary Report",
                    "url": "https://example.com/hiring-trends",
                    "snippet": "Average time-to-hire for software engineers: 42 days. Fully-loaded cost in US: $180-220K. Remote positions see 3x more applicants.",
                },
                {
                    "title": "Building High-Performance Engineering Teams",
                    "url": "https://example.com/eng-teams",
                    "snippet": "Optimal team growth rate: 25-30% per quarter. Beyond this, culture dilution and coordination overhead reduce productivity.",
                },
            ])

        if any(w in query_lower for w in ["ai", "machine learning", "technology"]):
            mock_results.extend([
                {
                    "title": "Enterprise AI Adoption Report 2024",
                    "url": "https://example.com/ai-adoption",
                    "snippet": "78% of enterprises are investing in AI. Average ROI timeline: 14-18 months. Top use cases: customer service (32%), operations (28%), analytics (22%).",
                },
                {
                    "title": "AI Infrastructure Costs and Comparison",
                    "url": "https://example.com/ai-infrastructure",
                    "snippet": "Cloud GPU costs: $2-4/hour per A100. Self-hosted break-even: typically at $50K+/month API spend. Build vs buy inflection at 18 months.",
                },
            ])

        # Default results if no keywords matched
        if not mock_results:
            mock_results = [
                {
                    "title": "Business Strategy Best Practices",
                    "url": "https://example.com/business-strategy",
                    "snippet": "Successful strategic initiatives share three traits: clear metrics, executive sponsorship, and phased execution with stage gates.",
                },
                {
                    "title": "Decision-Making Frameworks for Executives",
                    "url": "https://example.com/decision-frameworks",
                    "snippet": "Data-driven decisions outperform intuition-based ones by 2.3x on average. Key: define success criteria before committing resources.",
                },
                {
                    "title": "Risk Management in Growing Companies",
                    "url": "https://example.com/risk-management",
                    "snippet": "Top risks for growth-stage companies: cash flow (34%), talent retention (28%), competitive pressure (21%), regulatory compliance (17%).",
                },
            ]

        return mock_results[:max_results]
