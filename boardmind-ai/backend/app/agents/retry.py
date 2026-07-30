"""Shared retry logic for all agent services.

Provides retry with exponential backoff for rate limits
and graceful fallback to mock responses on repeated failures.
"""

import asyncio
import json
import logging
import re
from typing import Any, Callable, Awaitable, TypeVar

from app.agents.llm_provider import LLMError

logger = logging.getLogger(__name__)

T = TypeVar("T")

MAX_RETRIES = 3
BASE_BACKOFF = 2.0
MAX_BACKOFF = 15.0


async def retry_llm_call(
    agent_id: str,
    llm_generate: Callable[..., Awaitable[str]],
    system_prompt: str,
    user_prompt: str,
    parse_fn: Callable[[str], T],
    fallback_fn: Callable[[], T],
) -> T:
    """Execute an LLM call with exponential backoff retry.

    - Rate limits (429): backoff and retry up to MAX_RETRIES
    - Parse errors: retry once
    - After all retries exhausted: fall back to mock response
    """
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw_response = await llm_generate(system_prompt, user_prompt)
            return parse_fn(raw_response)

        except LLMError as e:
            last_error = e
            error_msg = str(e)

            # Rate limit: exponential backoff
            if "429" in error_msg or "rate_limit" in error_msg.lower():
                backoff = min(BASE_BACKOFF * (2 ** (attempt - 1)), MAX_BACKOFF)
                # Parse suggested wait time from Groq error
                retry_match = re.search(r'try again in ([\d.]+)s', error_msg)
                if retry_match:
                    backoff = min(float(retry_match.group(1)) + 0.5, MAX_BACKOFF)
                logger.warning(
                    f"{agent_id}: rate limited (attempt {attempt}/{MAX_RETRIES}), "
                    f"backing off {backoff:.1f}s"
                )
                await asyncio.sleep(backoff)
                continue

            # Other LLM errors: retry once
            if attempt < MAX_RETRIES:
                logger.warning(f"{agent_id}: LLM error (attempt {attempt}), retrying")
                await asyncio.sleep(1)
                continue

        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as e:
            last_error = e
            if attempt < MAX_RETRIES:
                logger.warning(
                    f"{agent_id}: parse error (attempt {attempt}/{MAX_RETRIES}), retrying"
                )
                await asyncio.sleep(0.5)
                continue

    # All retries exhausted — fallback
    logger.error(
        f"{agent_id} failed after {MAX_RETRIES} attempts: {last_error}. "
        "Falling back to mock response."
    )
    return fallback_fn()
