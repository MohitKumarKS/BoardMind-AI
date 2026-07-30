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
    """Groq LLM provider with dual-key failover.

    Uses two Groq API keys (from different accounts) to double TPM capacity.
    When primary key hits rate limit, automatically switches to secondary.
    Configured via GROQ_API_KEY and GROQ_API_KEY_SECONDARY environment variables.
    """

    PRIMARY_MODEL = "llama-3.1-8b-instant"
    FALLBACK_MODEL = "llama-3.3-70b-versatile"

    def __init__(self):
        self._model: str = os.environ.get("GROQ_MODEL", self.PRIMARY_MODEL)
        self._primary_client = None
        self._secondary_client = None
        self._semaphore = asyncio.Semaphore(
            int(os.environ.get("LLM_MAX_CONCURRENT", "3"))
        )

    @property
    def is_configured(self) -> bool:
        api_key = os.environ.get("GROQ_API_KEY")
        return api_key is not None and len(api_key) > 0

    @property
    def _has_secondary(self) -> bool:
        key = os.environ.get("GROQ_API_KEY_SECONDARY")
        return key is not None and len(key) > 0

    def _get_primary_client(self):
        """Lazy-initialize the primary Groq client."""
        if self._primary_client is None:
            from groq import Groq
            self._primary_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        return self._primary_client

    def _get_secondary_client(self):
        """Lazy-initialize the secondary Groq client."""
        if self._secondary_client is None:
            from groq import Groq
            self._secondary_client = Groq(api_key=os.environ.get("GROQ_API_KEY_SECONDARY"))
        return self._secondary_client

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a JSON response from Groq with dual-key failover."""
        if not self.is_configured:
            raise LLMNotConfiguredError(
                "No Groq API key configured. Set GROQ_API_KEY environment variable."
            )

        async with self._semaphore:
            # Try primary key
            try:
                client = self._get_primary_client()
                return await self._call_groq(client, self._model, system_prompt, user_prompt)
            except LLMError as e:
                error_msg = str(e)

                # Rate limited on primary → try secondary key
                if ("429" in error_msg or "rate_limit" in error_msg.lower()) and self._has_secondary:
                    logger.info("Primary key rate limited, switching to secondary key")
                    try:
                        client2 = self._get_secondary_client()
                        return await self._call_groq(client2, self._model, system_prompt, user_prompt)
                    except LLMError as e2:
                        # Secondary also failed — propagate for retry logic
                        raise LLMError(f"Both keys exhausted: primary={error_msg[:50]}, secondary={str(e2)[:50]}")

                # Model error → try fallback model on primary
                if "model" in error_msg.lower() and self._model != self.FALLBACK_MODEL:
                    logger.warning(f"Primary model failed, trying fallback model")
                    try:
                        client = self._get_primary_client()
                        return await self._call_groq(client, self.FALLBACK_MODEL, system_prompt, user_prompt)
                    except LLMError:
                        pass  # Fall through to raise original

                raise

    async def _call_groq(
        self, client, model: str, system_prompt: str, user_prompt: str,
        max_tokens: int = 1024,
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
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise LLMError(f"Groq returned an empty response (model: {model})")

            return content

        except LLMError:
            raise
        except Exception as e:
            raise LLMError(f"Groq API error: {str(e)}")


class OpenAIProvider(BaseLLMProvider):
    """OpenAI-compatible LLM provider (legacy).

    Uses httpx to call OpenAI-compatible chat/completions endpoint.
    Configured via OPENAI_API_KEY environment variable.
    """

    def __init__(self):
        self._model: str = os.environ.get("OPENAI_MODEL", "gpt-4o")
        self._base_url: str = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

    @property
    def is_configured(self) -> bool:
        api_key = os.environ.get("OPENAI_API_KEY")
        return api_key is not None and len(api_key) > 0

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.is_configured:
            raise LLMNotConfiguredError(
                "No OpenAI API key configured. Set OPENAI_API_KEY environment variable."
            )

        try:
            import httpx

            api_key = os.environ.get("OPENAI_API_KEY")
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
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
    2. Otherwise: returns GroqProvider (which lazy-checks GROQ_API_KEY)
    3. If GROQ_API_KEY is not set at call time, GroqProvider.is_configured
       returns False and agents fall back to mock responses.

    Note: Provider checks env vars lazily at call time, not at construction.
    This ensures dotenv loading order doesn't matter.
    """
    override = os.environ.get("LLM_PROVIDER", "").lower()

    if override == "mock":
        return MockProvider()
    elif override == "openai":
        return OpenAIProvider()
    elif override == "groq":
        return GroqProvider()

    # Default: return GroqProvider which lazy-checks the key
    # This works even if GROQ_API_KEY isn't set yet at import time
    return GroqProvider()


# Backward-compatible alias
LLMProvider = get_provider
