"""Evidence extractor for mock responses.

Parses MCP evidence from agent context to extract key figures
that mock responses can reference in their analysis.
Used only by mock mode — real LLM agents handle evidence naturally.
"""

import re
from typing import Any


def extract_evidence_facts(context: str | None) -> dict[str, Any]:
    """Extract key business facts from MCP evidence in context.

    Returns a dict with extracted facts that mocks can use.
    Returns empty dict if no evidence is present.
    """
    if not context or "[Attached File:" not in context:
        return {}

    facts: dict[str, Any] = {}

    # Extract the evidence portion
    parts = context.split("[Attached File:", 1)
    evidence_text = parts[1] if len(parts) > 1 else ""

    # Extract filename
    filename_match = re.match(r"\s*([^\]]+)\]", evidence_text)
    if filename_match:
        facts["filename"] = filename_match.group(1).strip()

    # Extract total revenue/sales
    total_rev = re.search(r"Total (?:Revenue|Sales|revenue|sales)[:\s]*\$?([\d,.]+[MBKmk]?)", evidence_text)
    if total_rev:
        facts["total_revenue"] = total_rev.group(1)

    # Extract average values
    avg_match = re.search(r"Average (?:Revenue|revenue|Growth|growth|margin)[:\s]*\$?([\d,.]+[%MBK]?)", evidence_text)
    if avg_match:
        facts["average_metric"] = avg_match.group(1)

    # Extract highest performer
    highest = re.search(r"Highest (?:Revenue|revenue|growth)[:\s]*([^\n(]+)\(?([^)]*)\)?", evidence_text)
    if highest:
        facts["top_performer"] = highest.group(1).strip()
        if highest.group(2):
            facts["top_performer_value"] = highest.group(2).strip()

    # Extract lowest performer
    lowest = re.search(r"Lowest (?:Revenue|revenue|growth)[:\s]*([^\n(]+)\(?([^)]*)\)?", evidence_text)
    if lowest:
        facts["bottom_performer"] = lowest.group(1).strip()
        if lowest.group(2):
            facts["bottom_performer_value"] = lowest.group(2).strip()

    # Extract row count
    rows_match = re.search(r"(\d+)\s*rows", evidence_text)
    if rows_match:
        facts["data_rows"] = int(rows_match.group(1))

    # Extract columns
    cols_match = re.search(r"Columns?:\s*([^\n]+)", evidence_text)
    if cols_match:
        facts["columns"] = cols_match.group(1).strip()

    # Extract growth percentages
    growth_matches = re.findall(r"([\d.]+)%", evidence_text)
    if growth_matches:
        growth_vals = [float(g) for g in growth_matches[:10]]
        if growth_vals:
            facts["max_growth"] = f"{max(growth_vals):.1f}%"
            facts["min_growth"] = f"{min(growth_vals):.1f}%"
            facts["avg_growth"] = f"{sum(growth_vals) / len(growth_vals):.1f}%"

    # Check if we found any meaningful data
    facts["has_evidence"] = bool(facts.get("total_revenue") or facts.get("top_performer") or facts.get("data_rows"))

    return facts


def build_evidence_rationale_prefix(facts: dict[str, Any], department: str) -> str:
    """Build a department-specific opening paragraph referencing uploaded data.

    Args:
        facts: Extracted evidence facts from extract_evidence_facts().
        department: The department name (finance, marketing, etc.)

    Returns:
        A paragraph referencing the data, or empty string if no evidence.
    """
    if not facts.get("has_evidence"):
        return ""

    parts: list[str] = []

    if department == "finance":
        if facts.get("total_revenue"):
            parts.append(f"The uploaded data projects total revenue of ${facts['total_revenue']}")
        if facts.get("top_performer"):
            parts.append(f"with {facts['top_performer']} as the highest contributor")
        if facts.get("max_growth"):
            parts.append(f"and growth rates ranging from {facts.get('min_growth', 'N/A')} to {facts['max_growth']}")

    elif department == "marketing":
        if facts.get("top_performer"):
            parts.append(f"The uploaded data shows strongest demand in {facts['top_performer']}")
        if facts.get("data_rows"):
            parts.append(f"across {facts['data_rows']} segments/regions analyzed")
        if facts.get("max_growth"):
            parts.append(f"with projected growth up to {facts['max_growth']}")

    elif department == "sales":
        if facts.get("total_revenue"):
            parts.append(f"The uploaded forecast projects ${facts['total_revenue']} in total revenue opportunity")
        if facts.get("data_rows"):
            parts.append(f"spanning {facts['data_rows']} territories/accounts")
        if facts.get("top_performer"):
            parts.append(f"with highest demand concentrated in {facts['top_performer']}")

    elif department == "hr":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data covers {facts['data_rows']} regions/units requiring workforce planning")
        if facts.get("max_growth"):
            parts.append(f"with growth rates up to {facts['max_growth']} suggesting significant hiring needs")

    elif department == "operations":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data identifies {facts['data_rows']} operational regions/units to coordinate")
        if facts.get("top_performer"):
            parts.append(f"with highest volume in {facts['top_performer']}")
        if facts.get("total_revenue"):
            parts.append(f"supporting ${facts['total_revenue']} in projected throughput")

    elif department == "legal":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data involves {facts['data_rows']} jurisdictions/entities requiring compliance review")
        if facts.get("filename"):
            parts.append(f"based on the attached '{facts['filename']}'")

    elif department == "it":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data spans {facts['data_rows']} data points requiring infrastructure consideration")
        if facts.get("total_revenue"):
            parts.append(f"supporting a ${facts['total_revenue']} revenue operation that demands high availability")

    elif department == "business_analytics":
        if facts.get("total_revenue"):
            parts.append(f"The uploaded dataset provides empirical evidence: ${facts['total_revenue']} total projected value")
        if facts.get("max_growth"):
            parts.append(f"with growth ranging {facts.get('min_growth', 'N/A')} to {facts['max_growth']}")
        if facts.get("data_rows"):
            parts.append(f"across {facts['data_rows']} data points")
        if facts.get("top_performer"):
            parts.append(f"({facts['top_performer']} leads)")

    if not parts:
        return ""

    return ". ".join(parts) + ".\n\n"
