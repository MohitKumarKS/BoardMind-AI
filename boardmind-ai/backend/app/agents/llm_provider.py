"""LLM Provider abstraction for BoardMind AI.

Supports multiple backends:
- Groq (primary — Llama 3.3 70B)
- OpenAI-compatible (legacy)
- Mock mode (no key configured)

The provider is selected automatically based on environment variables:
- GROQ_API_KEY set → GroqProvider
- OPENAI_API_KEY set → OpenAIProvider
- Neither set → mock mode (agents use _generate_mock_response)

Override with LLM_PROVIDER=groq|openai|mock to force a specific backend.
"""

import asyncio
import logging
import os
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Raised when LLM invocation fails."""
    pass


class LLMNotConfiguredError(LLMError):
    """Raised when no LLM API key is configured."""
    pass


class BaseLLMProvider(ABC):
    """Abstract base for all LLM providers."""

    @property
    @abstractmethod
    def is_configured(self) -> bool:
        """Whether this provider has valid credentials configured."""
        ...

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response from the LLM.

        Args:
            system_prompt: The system prompt establishing the agent persona.
            user_prompt: The user's scenario and instructions.

        Returns:
            Raw string response from the LLM (expected to be JSON).

        Raises:
            LLMError: If the invocation fails.
            LLMNotConfiguredError: If credentials are missing.
        """
        ...


class GroqProvider(BaseLLMProvider):
    """Groq LLM provider using the official Groq Python SDK.

    Uses Llama 3.3 70B as the primary model with automatic fallback
    to Llama 3.1 8B if the primary model is unavailable.
    Configured via GROQ_API_KEY environment variable.
    """

    PRIMARY_MODEL = "llama-3.1-8b-instant"
    FALLBACK_MODEL = "llama-3.3-70b-versatile"

    def __init__(self):
        self._api_key: str | None = os.environ.get("GROQ_API_KEY")
        self._model: str = os.environ.get("GROQ_MODEL", self.PRIMARY_MODEL)
        self._client = None
        self._semaphore = asyncio.Semaphore(
            int(os.environ.get("LLM_MAX_CONCURRENT", "2"))
        )

    @property
    def is_configured(self) -> bool:
        return self._api_key is not None and len(self._api_key) > 0

    def _get_client(self):
        """Lazy-initialize the Groq client."""
        if self._client is None:
            from groq import Groq
            self._client = Groq(api_key=self._api_key)
        return self._client

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a JSON response from Groq/Llama."""
        if not self.is_configured:
            raise LLMNotConfiguredError(
                "No Groq API key configured. Set GROQ_API_KEY environment variable."
            )

        client = self._get_client()

        async with self._semaphore:
            # Try primary model first
            try:
                return await self._call_groq(client, self._model, system_prompt, user_prompt)
            except LLMError as e:
                error_msg = str(e)
                # If model not available, try fallback
                if "model" in error_msg.lower() and self._model != self.FALLBACK_MODEL:
                    logger.warning(
                        f"Primary model '{self._model}' failed, "
                        f"falling back to '{self.FALLBACK_MODEL}'"
                    )
                    return await self._call_groq(
                        client, self.FALLBACK_MODEL, system_prompt, user_prompt
                    )
                raise

    async def _call_groq(
        self, client, model: str, system_prompt: str, user_prompt: str
    ) -> str:
        """Execute a single Groq API call."""
        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=2048,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise LLMError(f"Groq returned an empty response (model: {model})")

            return content

        except LLMError:
            raise
        except Exception as e:
            error_msg = str(e)

            # Retry once on rate limit errors
            if "429" in error_msg or "rate_limit" in error_msg.lower():
                logger.warning(f"Groq rate limited, retrying in 8s...")
                await asyncio.sleep(8)
                try:
                    response = await asyncio.to_thread(
                        client.chat.completions.create,
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        temperature=0.3,
                        max_tokens=2048,
                        response_format={"type": "json_object"},
                    )
                    content = response.choices[0].message.content
                    if content:
                        return content
                    raise LLMError("Groq returned empty on retry")
                except LLMError:
                    raise
                except Exception as retry_e:
                    raise LLMError(f"Groq retry failed: {retry_e}")

            raise LLMError(f"Groq invocation failed: {error_msg}")


class OpenAIProvider(BaseLLMProvider):
    """OpenAI-compatible LLM provider (legacy).

    Uses httpx to call OpenAI-compatible chat/completions endpoint.
    Configured via OPENAI_API_KEY environment variable.
    """

    def __init__(self):
        self._api_key: str | None = os.environ.get("OPENAI_API_KEY")
        self._model: str = os.environ.get("OPENAI_MODEL", "gpt-4o")
        self._base_url: str = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

    @property
    def is_configured(self) -> bool:
        return self._api_key is not None and len(self._api_key) > 0

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.is_configured:
            raise LLMNotConfiguredError(
                "No OpenAI API key configured. Set OPENAI_API_KEY environment variable."
            )

        try:
            import httpx

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self._model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        "temperature": 0.3,
                        "response_format": {"type": "json_object"},
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except ImportError:
            raise LLMError("httpx is required for OpenAI. Install with: pip install httpx")
        except Exception as e:
            raise LLMError(f"OpenAI invocation failed: {str(e)}")


class MockProvider(BaseLLMProvider):
    """Mock provider that always reports as unconfigured.

    Forces agents into mock mode regardless of available API keys.
    Used for development/testing via LLM_PROVIDER=mock.
    """

    @property
    def is_configured(self) -> bool:
        return False

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise LLMNotConfiguredError("Mock mode — LLM calls disabled")


def get_provider() -> BaseLLMProvider:
    """Factory function that returns the appropriate LLM provider.

    Selection logic:
    1. LLM_PROVIDER env var forces a specific backend
    2. Otherwise: GROQ_API_KEY → Groq, OPENAI_API_KEY → OpenAI
    3. If neither key exists, returns MockProvider → mock mode
    """
    override = os.environ.get("LLM_PROVIDER", "").lower()

    if override == "mock":
        return MockProvider()
    elif override == "openai":
        return OpenAIProvider()
    elif override == "groq":
        return GroqProvider()

    # Auto-detect based on available keys
    if os.environ.get("GROQ_API_KEY"):
        return GroqProvider()
    elif os.environ.get("OPENAI_API_KEY"):
        return OpenAIProvider()

    # No keys — mock mode
    return MockProvider()


# Backward-compatible alias
LLMProvider = get_provider
