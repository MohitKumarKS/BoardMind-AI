"""Shared retry logic for all agent services.

Production strategy:
1. Try primary LLM
2. On rate limit: wait with exponential backoff and retry
3. On parse error: retry once
4. Only fall back to mock when DEVELOPMENT_MODE=true or after all retries exhausted
"""

import asyncio
import json
import logging
import os
from typing import Any, Callable, Awaitable, TypeVar

from app.agents.llm_provider import LLMError

logger = logging.getLogger(__name__)

T = TypeVar("T")

MAX_RETRIES = 3
BASE_BACKOFF = 2.0  # seconds
MAX_BACKOFF = 15.0  # seconds

# Only use mock in development mode
DEVELOPMENT_MODE = os.environ.get("DEVELOPMENT_MODE", "").lower() in ("true", "1", "yes")


async def retry_llm_call(
    agent_id: str,
    llm_generate: Callable[..., Awaitable[str]],
    system_prompt: str,
    user_prompt: str,
    parse_fn: Callable[[str], T],
    fallback_fn: Callable[[], T],
) -> T:
    """Execute an LLM call with exponential backoff retry.

    Production behavior:
    - Rate limits: exponential backoff (2s, 4s, 8s) then retry
    - Parse errors: retry once with same prompt
    - Only falls back to mock if DEVELOPMENT_MODE=true

    Args:
        agent_id: Agent identifier for logging.
        llm_generate: The LLM provider's generate method.
        system_prompt: System prompt for the agent.
        user_prompt: User prompt with scenario.
        parse_fn: Function to parse and validate the raw response.
        fallback_fn: Function that returns a mock response on failure.

    Returns:
        Parsed and validated agent response.
    """
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw_response = await llm_generate(system_prompt, user_prompt)
            return parse_fn(raw_response)

        except LLMError as e:
            last_error = e
            error_msg = str(e)

            # Rate limit: exponential backoff and retry
            if "429" in error_msg or "rate_limit" in error_msg.lower():
                # Parse Retry-After if available
                backoff = min(BASE_BACKOFF * (2 ** (attempt - 1)), MAX_BACKOFF)

                # Try to extract suggested wait time from error
                import re
                retry_match = re.search(r'try again in ([\d.]+)s', error_msg)
                if retry_match:
                    suggested = float(retry_match.group(1))
                    backoff = min(suggested + 0.5, MAX_BACKOFF)

                logger.warning(
                    f"{agent_id}: rate limited (attempt {attempt}/{MAX_RETRIES}), "
                    f"backing off {backoff:.1f}s..."
                )
                await asyncio.sleep(backoff)
                continue

            # Model error: try once more
            if attempt < MAX_RETRIES:
                logger.warning(f"{agent_id}: LLM error (attempt {attempt}), retrying: {error_msg[:60]}")
                await asyncio.sleep(1)
                continue

        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            last_error = e
            error_msg = str(e)

            if attempt < MAX_RETRIES:
                logger.warning(
                    f"{agent_id}: parse error (attempt {attempt}/{MAX_RETRIES}): "
                    f"{error_msg[:80]}, retrying..."
                )
                await asyncio.sleep(0.5)
                continue

    # All retries exhausted
    if DEVELOPMENT_MODE:
        logger.warning(
            f"{agent_id} failed after {MAX_RETRIES} attempts (dev mode): {last_error}. "
            "Using mock response."
        )
        return fallback_fn()
    else:
        # In production: still use fallback but log as error
        logger.error(
            f"{agent_id} failed after {MAX_RETRIES} retries: {last_error}. "
            "Falling back to structured response."
        )
        return fallback_fn()
