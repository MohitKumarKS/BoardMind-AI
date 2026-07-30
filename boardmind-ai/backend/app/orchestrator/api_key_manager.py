"""API Key Manager for BoardMind AI.

Manages multiple Groq API keys with health tracking, load balancing,
and automatic failover. Supports 1-N keys without code changes.
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class APIKeyState:
    """Health state of a single API key."""
    key: str
    index: int
    active_requests: int = 0
    total_requests: int = 0
    total_failures: int = 0
    total_rate_limits: int = 0
    last_rate_limit_time: float = 0.0
    cooldown_until: float = 0.0
    avg_latency_ms: float = 0.0
    _latency_samples: list = field(default_factory=list)

    @property
    def is_healthy(self) -> bool:
        """Key is healthy if not in cooldown."""
        return time.time() > self.cooldown_until

    @property
    def load_score(self) -> float:
        """Lower is better. Combines active requests + recent rate limits."""
        recency_penalty = 0
        if self.last_rate_limit_time > 0:
            seconds_since = time.time() - self.last_rate_limit_time
            if seconds_since < 30:
                recency_penalty = (30 - seconds_since) / 30 * 5
        return self.active_requests + recency_penalty

    def record_start(self):
        self.active_requests += 1
        self.total_requests += 1

    def record_success(self, latency_ms: float):
        self.active_requests = max(0, self.active_requests - 1)
        self._latency_samples.append(latency_ms)
        if len(self._latency_samples) > 20:
            self._latency_samples = self._latency_samples[-20:]
        self.avg_latency_ms = sum(self._latency_samples) / len(self._latency_samples)

    def record_failure(self):
        self.active_requests = max(0, self.active_requests - 1)
        self.total_failures += 1

    def record_rate_limit(self, cooldown_seconds: float = 10.0):
        self.active_requests = max(0, self.active_requests - 1)
        self.total_rate_limits += 1
        self.last_rate_limit_time = time.time()
        self.cooldown_until = time.time() + cooldown_seconds


class APIKeyManager:
    """Manages multiple API keys with load balancing and health tracking.

    Usage:
        manager = APIKeyManager()
        key_state = await manager.acquire_key()
        # ... use key_state.key ...
        manager.release_key(key_state, success=True, latency_ms=150)
    """

    def __init__(self):
        self._keys: list[APIKeyState] = []
        self._lock = asyncio.Lock()
        self._load_keys()

    def _load_keys(self):
        """Load all GROQ API keys from environment."""
        # Primary key
        primary = os.environ.get("GROQ_API_KEY", "")
        if primary:
            self._keys.append(APIKeyState(key=primary, index=0))

        # Secondary key
        secondary = os.environ.get("GROQ_API_KEY_SECONDARY", "")
        if secondary:
            self._keys.append(APIKeyState(key=secondary, index=1))

        # Additional keys (GROQ_API_KEY_2, GROQ_API_KEY_3, etc.)
        for i in range(2, 20):
            key = os.environ.get(f"GROQ_API_KEY_{i}", "")
            if key:
                self._keys.append(APIKeyState(key=key, index=i))

        logger.info(f"APIKeyManager: {len(self._keys)} keys loaded")

    @property
    def total_keys(self) -> int:
        return len(self._keys)

    @property
    def healthy_keys(self) -> int:
        return sum(1 for k in self._keys if k.is_healthy)

    async def acquire_key(self) -> Optional[APIKeyState]:
        """Acquire the best available API key (least busy, healthy).

        Returns None if no keys are available (all in cooldown).
        """
        async with self._lock:
            # Filter to healthy keys
            available = [k for k in self._keys if k.is_healthy]
            if not available:
                # All keys in cooldown — return the one with earliest cooldown end
                if self._keys:
                    soonest = min(self._keys, key=lambda k: k.cooldown_until)
                    wait_time = soonest.cooldown_until - time.time()
                    if wait_time > 0:
                        logger.warning(f"All keys in cooldown, waiting {wait_time:.1f}s")
                        # Release lock during wait
                        self._lock.release()
                        await asyncio.sleep(wait_time)
                        await self._lock.acquire()
                    soonest.record_start()
                    return soonest
                return None

            # Select least busy key
            best = min(available, key=lambda k: k.load_score)
            best.record_start()
            return best

    def release_key(self, key_state: APIKeyState, success: bool = True, latency_ms: float = 0, rate_limited: bool = False, cooldown: float = 10.0):
        """Release a key after use."""
        if rate_limited:
            key_state.record_rate_limit(cooldown)
        elif success:
            key_state.record_success(latency_ms)
        else:
            key_state.record_failure()

    def get_stats(self) -> dict:
        """Return stats for logging."""
        return {
            "total_keys": self.total_keys,
            "healthy_keys": self.healthy_keys,
            "keys": [
                {
                    "index": k.index,
                    "healthy": k.is_healthy,
                    "active": k.active_requests,
                    "total": k.total_requests,
                    "rate_limits": k.total_rate_limits,
                    "avg_latency_ms": round(k.avg_latency_ms),
                }
                for k in self._keys
            ],
        }
