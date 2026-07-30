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

    # --- New 12 agents: generic evidence prefix based on available data ---
    elif department == "ceo":
        if facts.get("total_revenue"):
            parts.append(f"The uploaded data indicates a ${facts['total_revenue']} revenue operation")
        if facts.get("data_rows"):
            parts.append(f"spanning {facts['data_rows']} data points for strategic consideration")
        if facts.get("max_growth"):
            parts.append(f"with growth potential up to {facts['max_growth']}")

    elif department == "ciso":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data involves {facts['data_rows']} records requiring security assessment")
        if facts.get("total_revenue"):
            parts.append(f"protecting a ${facts['total_revenue']} revenue stream from cyber threats")

    elif department == "risk":
        if facts.get("total_revenue"):
            parts.append(f"The uploaded data shows ${facts['total_revenue']} total value at risk")
        if facts.get("max_growth") and facts.get("min_growth"):
            parts.append(f"with variance from {facts['min_growth']} to {facts['max_growth']} indicating exposure range")
        if facts.get("data_rows"):
            parts.append(f"across {facts['data_rows']} risk factors")

    elif department == "compliance":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data spans {facts['data_rows']} items requiring compliance review")
        if facts.get("filename"):
            parts.append(f"sourced from '{facts['filename']}'")

    elif department == "strategy":
        if facts.get("total_revenue"):
            parts.append(f"The uploaded data projects ${facts['total_revenue']} in addressable opportunity")
        if facts.get("top_performer"):
            parts.append(f"with {facts['top_performer']} as the leading segment")
        if facts.get("max_growth"):
            parts.append(f"and growth ceiling at {facts['max_growth']}")

    elif department == "product":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data covers {facts['data_rows']} product data points")
        if facts.get("top_performer"):
            parts.append(f"with highest demand in {facts['top_performer']}")
        if facts.get("max_growth"):
            parts.append(f"showing {facts['max_growth']} peak adoption growth")

    elif department == "customer_success":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data tracks {facts['data_rows']} customer data points")
        if facts.get("top_performer"):
            parts.append(f"with strongest performance in {facts['top_performer']}")
        if facts.get("average_metric"):
            parts.append(f"and average metrics at {facts['average_metric']}")

    elif department == "supply_chain":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data covers {facts['data_rows']} supply chain nodes")
        if facts.get("top_performer"):
            parts.append(f"with highest throughput in {facts['top_performer']}")
        if facts.get("total_revenue"):
            parts.append(f"supporting ${facts['total_revenue']} in operations value")

    elif department == "esg":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data includes {facts['data_rows']} sustainability data points")
        if facts.get("max_growth"):
            parts.append(f"with metrics ranging up to {facts['max_growth']}")

    elif department == "ai_governance":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data encompasses {facts['data_rows']} records for AI governance review")
        if facts.get("filename"):
            parts.append(f"from source '{facts['filename']}'")

    elif department == "innovation":
        if facts.get("data_rows"):
            parts.append(f"The uploaded data reveals {facts['data_rows']} innovation-relevant data points")
        if facts.get("max_growth"):
            parts.append(f"with growth potential reaching {facts['max_growth']}")
        if facts.get("top_performer"):
            parts.append(f"led by {facts['top_performer']}")

    elif department == "investor_relations":
        if facts.get("total_revenue"):
            parts.append(f"The uploaded data shows ${facts['total_revenue']} in total value for investor communications")
        if facts.get("max_growth"):
            parts.append(f"with growth trajectory up to {facts['max_growth']}")
        if facts.get("top_performer"):
            parts.append(f"driven primarily by {facts['top_performer']}")

    if not parts:
        return ""

    return ". ".join(parts) + ".\n\n"
