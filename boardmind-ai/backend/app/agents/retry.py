"""Shared retry logic for all agent services.

Provides a decorator/helper that wraps LLM invocation with retry
and graceful fallback to mock responses on repeated failures.

Defect fixed: Only the Analytics agent had retry logic. All other
agents would crash on Groq JSON validation failures, truncated
responses, or transient LLM errors.
"""

import json
import logging
from typing import Any, Callable, Awaitable, TypeVar

from app.agents.llm_provider import LLMError

logger = logging.getLogger(__name__)

T = TypeVar("T")

MAX_RETRIES = 2


async def retry_llm_call(
    agent_id: str,
    llm_generate: Callable[..., Awaitable[str]],
    system_prompt: str,
    user_prompt: str,
    parse_fn: Callable[[str], T],
    fallback_fn: Callable[[], T],
) -> T:
    """Execute an LLM call with retry and fallback.

    Args:
        agent_id: Agent identifier for logging.
        llm_generate: The LLM provider's generate method.
        system_prompt: System prompt for the agent.
        user_prompt: User prompt with scenario.
        parse_fn: Function to parse and validate the raw response.
        fallback_fn: Function that returns a mock response on failure.

    Returns:
        Parsed and validated agent response, or mock fallback.
    """
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw_response = await llm_generate(system_prompt, user_prompt)
            return parse_fn(raw_response)
        except (LLMError, json.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            last_error = e
            error_msg = str(e)

            if "json_validate_failed" in error_msg or "failed_generation" in error_msg:
                logger.warning(
                    f"{agent_id} agent: Groq JSON validation failed "
                    f"(attempt {attempt}/{MAX_RETRIES}), retrying..."
                )
            elif isinstance(e, (json.JSONDecodeError, ValueError, TypeError, KeyError)):
                logger.warning(
                    f"{agent_id} agent: parse error "
                    f"(attempt {attempt}/{MAX_RETRIES}): {error_msg}, retrying..."
                )
            else:
                # Non-retryable LLM error (auth failure, etc.)
                raise

    # All retries exhausted — fall back to mock
    logger.error(
        f"{agent_id} agent failed after {MAX_RETRIES} attempts: {last_error}. "
        "Falling back to mock response."
    )
    return fallback_fn()
