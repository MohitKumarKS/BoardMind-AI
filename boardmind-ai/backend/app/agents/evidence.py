"""Shared MCP Evidence injection for agent prompts.

Provides a helper that appends a structured "Evidence From Uploaded Data"
section to agent prompts when MCP evidence is present in the context string.

This module is used by all department agent prompt builders.
When no evidence is present, it returns the context unchanged.
"""

# Marker that the frontend/orchestrator injects to separate user context from evidence
EVIDENCE_MARKER = "[Attached File:"


def build_evidence_section(context: str | None) -> tuple[str | None, str | None]:
    """Split context into user context and MCP evidence.

    Args:
        context: The raw context string which may contain MCP evidence.

    Returns:
        Tuple of (user_context, evidence_section).
        Either or both may be None.
    """
    if not context:
        return None, None

    if EVIDENCE_MARKER not in context:
        return context.strip() or None, None

    # Split at the marker
    parts = context.split(EVIDENCE_MARKER, 1)
    user_context = parts[0].strip() or None
    raw_evidence = EVIDENCE_MARKER + parts[1]

    return user_context, raw_evidence.strip()


def format_prompt_with_evidence(
    scenario: str,
    context: str | None,
    role_instruction: str,
    max_evidence_chars: int = 800,
) -> str:
    """Build a complete user prompt with separated evidence section.

    This is the shared prompt builder used by all agents. It:
    1. Presents the business proposal
    2. Shows additional user context (if any)
    3. Presents MCP evidence (truncated to fit token limits)
    4. Adds role-specific analysis instructions

    Args:
        scenario: The business proposal text.
        context: Optional context (may contain MCP evidence).
        role_instruction: Agent-specific instructions paragraph.
        max_evidence_chars: Maximum characters for the evidence section.

    Returns:
        Complete formatted prompt string.
    """
    user_context, evidence = build_evidence_section(context)

    # Truncate scenario to reduce token usage
    if len(scenario) > 600:
        scenario = scenario[:600] + "..."

    prompt = f"""Analyze the following business proposal.

## Business Proposal

{scenario}"""

    if user_context:
        # Truncate user context to minimize tokens
        truncated_context = user_context[:300] if len(user_context) > 300 else user_context
        prompt += f"""

## Additional Context

{truncated_context}"""

    if evidence:
        # Truncate evidence to fit within token limits
        truncated_evidence = evidence[:max_evidence_chars]
        if len(evidence) > max_evidence_chars:
            truncated_evidence += "\n[... additional data truncated for brevity]"

        prompt += f"""

## Evidence From Uploaded Data

Reference these numbers in your analysis:

{truncated_evidence}"""

    prompt += f"""

## Instructions

{role_instruction}
"""

    return prompt
