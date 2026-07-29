"""MCP Context Summarizer.

Generates structured business summaries from uploaded MCP data.
The summary is generated ONCE per uploaded file and reused across
all department agents during the meeting.

For tabular data (CSV/Excel): extracts key metrics, rankings, trends.
For document data (PDF/DOCX/TXT): extracts key business facts and figures.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def summarize_mcp_data(mcp_result: dict[str, Any]) -> str:
    """Generate a structured evidence summary from MCP extraction result.

    Args:
        mcp_result: The result dict returned by MCP registry tools
                    (read_spreadsheet or read_file).

    Returns:
        A formatted text summary suitable for injection into agent prompts.
        Returns empty string if data cannot be summarized.
    """
    source_type = mcp_result.get("source_type") or mcp_result.get("source", "")

    if source_type in ("csv", "excel") or "data" in mcp_result:
        return _summarize_tabular(mcp_result)
    elif mcp_result.get("text"):
        return _summarize_document(mcp_result)
    else:
        return ""


def _summarize_tabular(result: dict[str, Any]) -> str:
    """Summarize tabular data (CSV/Excel) into key business metrics."""
    columns = result.get("columns", [])
    data = result.get("data", [])
    total_rows = result.get("total_rows", len(data))
    numeric_summary = result.get("numeric_summary", {})
    filename = result.get("filename", "uploaded file")

    if not data or not columns:
        return ""

    lines: list[str] = []
    lines.append(f"Source: {filename} ({total_rows} rows, {len(columns)} columns)")
    lines.append(f"Columns: {', '.join(columns)}")
    lines.append("")

    # Identify key column types by name heuristics
    revenue_cols = [c for c in columns if any(kw in c.lower() for kw in ("revenue", "sales", "income", "amount", "value", "price", "cost", "budget"))]
    growth_cols = [c for c in columns if any(kw in c.lower() for kw in ("growth", "change", "increase", "rate", "margin", "percent", "pct"))]
    quantity_cols = [c for c in columns if any(kw in c.lower() for kw in ("quantity", "units", "count", "demand", "volume", "headcount", "fte"))]
    label_cols = [c for c in columns if any(kw in c.lower() for kw in ("name", "region", "product", "department", "category", "segment", "market", "country", "city", "team", "customer"))]
    satisfaction_cols = [c for c in columns if any(kw in c.lower() for kw in ("satisfaction", "nps", "score", "rating"))]

    # Compute aggregates for numeric columns
    for col_name in revenue_cols + growth_cols + quantity_cols + satisfaction_cols:
        values = []
        for row in data:
            val = row.get(col_name)
            if val is not None:
                try:
                    values.append(float(val))
                except (ValueError, TypeError):
                    pass

        if not values:
            continue

        total = sum(values)
        avg = total / len(values)
        min_val = min(values)
        max_val = max(values)

        # Format based on column type
        if col_name in revenue_cols:
            if total > 1_000_000:
                lines.append(f"Total {col_name}: ${total / 1_000_000:.2f}M")
            elif total > 1_000:
                lines.append(f"Total {col_name}: ${total / 1_000:.1f}K")
            else:
                lines.append(f"Total {col_name}: ${total:,.0f}")
            lines.append(f"Average {col_name}: ${avg:,.0f}")
            lines.append(f"Range: ${min_val:,.0f} to ${max_val:,.0f}")
        elif col_name in growth_cols:
            lines.append(f"Average {col_name}: {avg:.1f}%")
            lines.append(f"Highest {col_name}: {max_val:.1f}%")
            lines.append(f"Lowest {col_name}: {min_val:.1f}%")
        elif col_name in satisfaction_cols:
            lines.append(f"Average {col_name}: {avg:.1f}")
            lines.append(f"Highest {col_name}: {max_val:.1f}")
            lines.append(f"Lowest {col_name}: {min_val:.1f}")
        else:
            if total > 1_000_000:
                lines.append(f"Total {col_name}: {total / 1_000_000:.2f}M")
            elif total > 1_000:
                lines.append(f"Total {col_name}: {total / 1_000:.1f}K")
            else:
                lines.append(f"Total {col_name}: {total:,.0f}")
            lines.append(f"Average {col_name}: {avg:,.0f}")

    # Find top/bottom performers using label + revenue columns
    if label_cols and revenue_cols:
        label_col = label_cols[0]
        rev_col = revenue_cols[0]

        # Sort by revenue descending
        sorted_rows = sorted(
            [r for r in data if r.get(rev_col) is not None],
            key=lambda r: float(r.get(rev_col, 0)),
            reverse=True,
        )

        if sorted_rows:
            lines.append("")
            top = sorted_rows[0]
            top_val = float(top.get(rev_col, 0))
            if top_val > 1_000_000:
                lines.append(f"Highest {rev_col}: {top.get(label_col)} (${top_val / 1_000_000:.2f}M)")
            else:
                lines.append(f"Highest {rev_col}: {top.get(label_col)} (${top_val:,.0f})")

            if len(sorted_rows) > 1:
                bottom = sorted_rows[-1]
                bot_val = float(bottom.get(rev_col, 0))
                if bot_val > 1_000_000:
                    lines.append(f"Lowest {rev_col}: {bottom.get(label_col)} (${bot_val / 1_000_000:.2f}M)")
                else:
                    lines.append(f"Lowest {rev_col}: {bottom.get(label_col)} (${bot_val:,.0f})")

    # Top performers by growth
    if label_cols and growth_cols:
        label_col = label_cols[0]
        growth_col = growth_cols[0]

        sorted_growth = sorted(
            [r for r in data if r.get(growth_col) is not None],
            key=lambda r: float(r.get(growth_col, 0)),
            reverse=True,
        )

        if sorted_growth:
            top_g = sorted_growth[0]
            lines.append(f"Highest growth: {top_g.get(label_col)} ({float(top_g.get(growth_col, 0)):.1f}%)")
            if len(sorted_growth) > 1:
                bot_g = sorted_growth[-1]
                lines.append(f"Lowest growth: {bot_g.get(label_col)} ({float(bot_g.get(growth_col, 0)):.1f}%)")

    # Top 5 records preview
    if data and label_cols:
        lines.append("")
        lines.append(f"Top {min(5, len(data))} records:")
        label_col = label_cols[0]
        preview_cols = [label_col] + revenue_cols[:1] + growth_cols[:1]
        for row in data[:5]:
            parts = []
            for c in preview_cols:
                val = row.get(c)
                if val is not None:
                    parts.append(f"{c}={val}")
            lines.append(f"  - {', '.join(parts)}")

    summary = "\n".join(lines)
    logger.info(f"MCP tabular summary generated: {len(lines)} lines from {filename}")
    return summary


def _summarize_document(result: dict[str, Any]) -> str:
    """Summarize document data (PDF/DOCX/TXT) into key business facts."""
    text = result.get("text", "")
    filename = result.get("filename", "uploaded document")
    char_count = result.get("char_count", len(text))
    fmt = result.get("format", "text")

    if not text.strip():
        return ""

    lines: list[str] = []
    lines.append(f"Source: {filename} ({fmt}, {char_count:,} characters)")
    lines.append("")

    # Extract key content - take first 3000 chars as the most relevant
    content = text[:3000].strip()

    # Try to extract numbers and financial figures
    import re

    # Find monetary values
    money_pattern = r'\$[\d,]+(?:\.\d+)?[MBKmk]?|\d+(?:,\d+)*(?:\.\d+)?\s*(?:million|billion|thousand|M\b|B\b|K\b)'
    money_matches = re.findall(money_pattern, content)
    if money_matches:
        lines.append("Financial figures mentioned:")
        for match in money_matches[:8]:
            lines.append(f"  - {match.strip()}")

    # Find percentages
    pct_pattern = r'\d+(?:\.\d+)?%'
    pct_matches = re.findall(pct_pattern, content)
    if pct_matches:
        lines.append("Percentages mentioned:")
        for match in pct_matches[:6]:
            lines.append(f"  - {match}")

    # Find timeline references
    time_pattern = r'(?:Q[1-4]\s*\d{4}|\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{4}|\d+\s*(?:months?|years?|weeks?|days?))'
    time_matches = re.findall(time_pattern, content)
    if time_matches:
        unique_times = list(dict.fromkeys(time_matches))[:5]
        lines.append("Timeline references:")
        for match in unique_times:
            lines.append(f"  - {match}")

    # Include condensed content as context
    lines.append("")
    lines.append("Document content (excerpt):")
    # Take first ~1500 chars, split into paragraphs
    paragraphs = [p.strip() for p in content[:1500].split("\n") if p.strip()]
    for para in paragraphs[:15]:
        if len(para) > 200:
            para = para[:200] + "..."
        lines.append(f"  {para}")

    summary = "\n".join(lines)
    logger.info(f"MCP document summary generated: {len(lines)} lines from {filename}")
    return summary
