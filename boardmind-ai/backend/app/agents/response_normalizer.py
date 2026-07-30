"""Response normalizer for LLM outputs.

Handles ALL common LLM formatting issues before Pydantic validation:
- LLM copies schema placeholders as literal values
- Returns lists instead of strings
- Returns dicts instead of strings
- Returns dicts instead of list-of-strings
"""

from typing import Any


# Valid enum values for position field
VALID_POSITIONS = {"support", "oppose", "neutral", "conditional"}

# Valid enum values for other fields
VALID_ENUMS = {
    "risk_level": {"low", "medium", "high"},
    "brand_impact": {"positive", "negative", "neutral"},
    "competitive_position": {"strengthened", "weakened", "unchanged"},
    "go_to_market_complexity": {"low", "medium", "high"},
    "pipeline_impact": {"new pipeline", "acceleration", "disruption"},
    "deal_cycle_effect": {"shorter", "longer", "unchanged"},
    "competitive_effect": {"advantage", "disadvantage", "neutral"},
    "headcount_change": {"hiring", "reduction", "redeployment", "none"},
    "skill_gap": {"none", "minor", "significant"},
    "culture_impact": {"positive", "negative", "neutral"},
    "change_complexity": {"low", "medium", "high"},
    "execution_complexity": {"low", "medium", "high"},
    "capacity_impact": {"within capacity", "stretch", "overload"},
    "compliance_status": {"compliant", "non-compliant", "requires_review"},
    "ip_implications": {"none", "minor", "significant"},
    "feasibility": {"straightforward", "moderate", "complex", "infeasible"},
    "security_risk": {"low", "medium", "high", "critical"},
    "infrastructure_needs": {"existing", "minor_additions", "significant_investment"},
    "integration_complexity": {"low", "medium", "high"},
    "technical_debt_impact": {"reduces", "neutral", "increases"},
    "evidence_strength": {"strong", "moderate", "weak", "insufficient"},
    "data_availability": {"available", "partially_available", "not_available"},
    "projection_confidence": {"high", "medium", "low"},
}


def _to_string(value: Any) -> str:
    """Convert any value to a clean string."""
    if isinstance(value, str):
        return value
    elif isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                parts.append(" ".join(str(v) for v in item.values()))
            else:
                parts.append(str(item))
        return "\n\n".join(parts)
    elif isinstance(value, dict):
        parts = []
        for k, v in value.items():
            if isinstance(v, str):
                parts.append(f"{k}: {v}")
            elif isinstance(v, list):
                parts.append(f"{k}: {', '.join(str(i) for i in v)}")
            else:
                parts.append(f"{k}: {v}")
        return "\n".join(parts)
    else:
        return str(value)


def _to_string_list(value: Any) -> list[str]:
    """Convert any value to a list of strings."""
    if not isinstance(value, list):
        return [_to_string(value)]

    result = []
    for item in value:
        if isinstance(item, dict):
            # Common patterns: {"phase": "...", "description": "..."}
            if "phase" in item:
                desc = item.get("description", item.get("details", ""))
                result.append(f"{item['phase']}: {desc}" if desc else str(item["phase"]))
            elif "risk" in item:
                result.append(str(item["risk"]))
            elif "action" in item:
                result.append(str(item["action"]))
            else:
                result.append(" - ".join(str(v) for v in item.values()))
        elif isinstance(item, list):
            result.append(", ".join(str(i) for i in item))
        else:
            result.append(str(item))
    return result


def _fix_enum_value(value: str, valid_values: set[str]) -> str:
    """Fix an enum value that might be a schema placeholder or descriptive text."""
    if not isinstance(value, str):
        value = str(value)

    # If it's already valid, return as-is
    lower = value.lower().strip()
    if lower in valid_values:
        return lower

    # LLM copied the schema placeholder like "support | oppose | neutral | conditional"
    # Try to extract the first valid value
    if "|" in value:
        parts = [p.strip().lower() for p in value.split("|")]
        for p in parts:
            if p in valid_values:
                return p
        # Default to first valid value (sorted for determinism)
        return sorted(valid_values)[0]

    # Descriptive text — find which valid value it contains
    for valid in valid_values:
        if valid in lower:
            return valid

    # Last resort — return first valid value (sorted for determinism)
    return sorted(valid_values)[0]


def normalize_agent_response(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize LLM output to match Pydantic schemas exactly.

    Handles:
    - Position as schema placeholder → extract valid enum
    - String fields returned as list/dict → convert to string
    - List fields returned as list of dicts → convert to list of strings
    - Enum fields with descriptive text → normalize to valid value
    """

    # Fix position field (most critical)
    if "position" in data:
        pos = data["position"]
        if not isinstance(pos, str) or pos.lower().strip() not in VALID_POSITIONS:
            data["position"] = _fix_enum_value(str(pos), VALID_POSITIONS)
        else:
            data["position"] = pos.lower().strip()

    # Fix confidence (ensure float)
    if "confidence" in data:
        try:
            data["confidence"] = float(data["confidence"])
        except (ValueError, TypeError):
            data["confidence"] = 0.5

    # Fields that MUST be strings
    string_fields = [
        "rationale", "summary", "measurement_plan",
        "customer_impact", "effort_estimate",
    ]
    for field in string_fields:
        if field in data and not isinstance(data[field], str):
            data[field] = _to_string(data[field])

    # Fields that MUST be list of strings
    list_string_fields = [
        "risks", "conditions", "metrics_to_track",
        "implementation_phases", "change_management_needs",
        "recommended_actions", "required_safeguards",
    ]
    for field in list_string_fields:
        if field in data:
            if not isinstance(data[field], list):
                data[field] = [_to_string(data[field])]
            else:
                data[field] = _to_string_list(data[field])

    # Fix domain_assessment enum fields
    if "domain_assessment" in data and isinstance(data["domain_assessment"], dict):
        da = data["domain_assessment"]

        for field, valid_values in VALID_ENUMS.items():
            if field in da:
                val = da[field]
                if isinstance(val, str):
                    da[field] = _fix_enum_value(val, valid_values)

        # Fix domain_assessment list fields
        da_list_fields = [
            "dependencies", "customer_segments_affected",
            "key_metrics", "benchmarks", "regulatory_bodies",
        ]
        for field in da_list_fields:
            if field in da:
                if not isinstance(da[field], list):
                    da[field] = [_to_string(da[field])]
                else:
                    da[field] = _to_string_list(da[field])

        # Fix domain_assessment string fields
        da_string_fields = [
            "revenue_impact", "cost_impact", "roi_estimate",
            "payback_period", "timeline_estimate", "resource_requirements",
            "market_opportunity", "revenue_upside", "revenue_risk",
            "liability_exposure", "timeline_to_readiness",
        ]
        for field in da_string_fields:
            if field in da and not isinstance(da[field], str):
                da[field] = _to_string(da[field])

    return data
