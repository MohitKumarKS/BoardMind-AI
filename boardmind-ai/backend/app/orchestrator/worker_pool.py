"""Dynamic Worker Pool for BoardMind AI.

Replaces wave-based scheduling with a pool of async workers
that continuously dequeue and execute tasks until the queue is empty.
"""

import asyncio
import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Optional

from app.orchestrator.api_key_manager import APIKeyManager, APIKeyState

logger = logging.getLogger(__name__)

# Configuration
NUM_WORKERS = int(os.environ.get("WORKER_POOL_SIZE", "5"))
WORKER_TIMEOUT = float(os.environ.get("WORKER_TIMEOUT", "40.0"))
STAGGER_INTERVAL = float(os.environ.get("WORKER_STAGGER", "0.8"))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
BASE_BACKOFF = 2.0
MAX_BACKOFF = 15.0


# Priority tiers
PRIORITY_TIERS: dict[str, int] = {
    # Tier 1 (highest priority = 1)
    "ceo": 1, "finance": 1, "it": 1, "operations": 1, "ciso": 1, "risk": 1,
    # Tier 2
    "marketing": 2, "hr": 2, "legal": 2, "strategy": 2, "business_analytics": 2, "compliance": 2,
    # Tier 3
    "product": 3, "customer_success": 3, "supply_chain": 3, "esg": 3,
    "ai_governance": 3, "innovation": 3, "investor_relations": 3, "sales": 3,
}


@dataclass
class ExecutiveTask:
    """A single executive task in the queue."""
    agent_id: str
    priority: int
    service: Any
    request: Any
    enqueued_at: float = 0.0

    def __lt__(self, other):
        """For priority queue ordering (lower priority number = higher priority)."""
        return self.priority < other.priority


@dataclass
class ExecutiveResult:
    """Result from executing a single executive."""
    agent_id: str
    status: str  # completed | failed | timeout
    response: Optional[dict] = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    queue_wait_ms: int = 0
    worker_id: int = 0
    key_index: int = -1
    retry_count: int = 0
    tokens_used: int = 0


class WorkerPool:
    """Dynamic async worker pool for executive agent execution.

    Workers continuously dequeue tasks and execute them using
    the API Key Manager for load-balanced key allocation.
    No worker ever sits idle while tasks remain in the queue.
    """

    def __init__(self, key_manager: APIKeyManager):
        self._key_manager = key_manager
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._results: list[ExecutiveResult] = []
        self._results_lock = asyncio.Lock()
        self._total_enqueued = 0

    async def execute_all(
        self,
        tasks: list[ExecutiveTask],
        board_context_updater=None,
    ) -> list[ExecutiveResult]:
        """Execute all tasks using the worker pool.

        Args:
            tasks: List of ExecutiveTask to execute.
            board_context_updater: Optional async callback(agent_id, status, response, time_ms)

        Returns:
            List of ExecutiveResult for all tasks.
        """
        self._results = []
        self._total_enqueued = len(tasks)

        # Enqueue all tasks with priority
        for task in tasks:
            task.enqueued_at = time.time()
            await self._queue.put((task.priority, task))

        # Determine effective worker count (no more workers than tasks)
        effective_workers = min(NUM_WORKERS, len(tasks))
        logger.info(f"WorkerPool: {len(tasks)} tasks queued, {effective_workers} workers starting")

        # Start workers with stagger
        workers = []
        for i in range(effective_workers):
            worker = asyncio.create_task(
                self._worker(i, board_context_updater)
            )
            workers.append(worker)
            if i < effective_workers - 1:
                await asyncio.sleep(STAGGER_INTERVAL)

        # Wait for all workers to finish (they stop when queue is empty)
        await asyncio.gather(*workers)

        # Performance summary
        completed = [r for r in self._results if r.status == "completed"]
        failed = [r for r in self._results if r.status != "completed"]
        if completed:
            times = [r.execution_time_ms for r in completed]
            logger.info(
                f"WorkerPool: {len(completed)}/{self._total_enqueued} succeeded | "
                f"avg={sum(times)//len(times)}ms | "
                f"fastest={min(times)}ms | slowest={max(times)}ms | "
                f"retries={sum(r.retry_count for r in self._results)}"
            )
        if failed:
            logger.warning(f"WorkerPool: Failed: {[r.agent_id for r in failed]}")

        return self._results

    async def _worker(self, worker_id: int, board_context_updater):
        """Worker loop: dequeue and execute until queue is empty."""
        while True:
            try:
                # Non-blocking get with timeout
                priority, task = await asyncio.wait_for(
                    self._queue.get(), timeout=2.0
                )
            except asyncio.TimeoutError:
                # Queue empty, worker done
                break

            result = await self._execute_task(worker_id, task)

            # Update board context if callback provided
            if board_context_updater:
                try:
                    await board_context_updater(
                        result.agent_id, result.status,
                        result.response, result.execution_time_ms, result.error
                    )
                except Exception as e:
                    logger.error(f"Worker {worker_id}: board context update failed: {e}")

            async with self._results_lock:
                self._results.append(result)

            self._queue.task_done()

    async def _execute_task(self, worker_id: int, task: ExecutiveTask) -> ExecutiveResult:
        """Execute a single task with retry logic."""
        queue_wait = int((time.time() - task.enqueued_at) * 1000)
        start = time.time()
        last_error = ""
        retry_count = 0

        for attempt in range(1, MAX_RETRIES + 1):
            llm_start = time.time()

            try:
                # Execute the agent with timeout
                response = await asyncio.wait_for(
                    task.service.analyze(task.request),
                    timeout=WORKER_TIMEOUT,
                )
                latency = (time.time() - llm_start) * 1000
                elapsed = int((time.time() - start) * 1000)

                logger.info(
                    f"Worker {worker_id}: {task.agent_id} completed in {elapsed}ms "
                    f"(retries={retry_count})"
                )

                return ExecutiveResult(
                    agent_id=task.agent_id,
                    status="completed",
                    response=response.model_dump(),
                    execution_time_ms=elapsed,
                    queue_wait_ms=queue_wait,
                    worker_id=worker_id,
                    retry_count=retry_count,
                )

            except asyncio.TimeoutError:
                last_error = f"Timeout after {WORKER_TIMEOUT}s"
                retry_count += 1
                logger.warning(f"Worker {worker_id}: {task.agent_id} timed out (attempt {attempt})")

            except Exception as e:
                error_msg = str(e)
                retry_count += 1

                # Rate limit — backoff and retry
                if "429" in error_msg or "rate_limit" in error_msg.lower():
                    cooldown = 10.0
                    match = re.search(r'try again in ([\d.]+)s', error_msg)
                    if match:
                        cooldown = float(match.group(1)) + 1.0
                    last_error = f"Rate limited"
                    logger.info(f"Worker {worker_id}: {task.agent_id} rate limited, waiting {cooldown:.0f}s")
                    await asyncio.sleep(cooldown)
                    continue

                # Other errors
                last_error = error_msg[:200]
                logger.warning(f"Worker {worker_id}: {task.agent_id} error (attempt {attempt}): {error_msg[:80]}")

                # Exponential backoff for retries
                if attempt < MAX_RETRIES:
                    backoff = min(BASE_BACKOFF * (2 ** (attempt - 1)), MAX_BACKOFF)
                    await asyncio.sleep(backoff)

        # All retries exhausted
        elapsed = int((time.time() - start) * 1000)
        logger.error(f"Worker {worker_id}: {task.agent_id} FAILED after {MAX_RETRIES} attempts: {last_error}")

        return ExecutiveResult(
            agent_id=task.agent_id,
            status="failed",
            error=last_error,
            execution_time_ms=elapsed,
            queue_wait_ms=queue_wait,
            worker_id=worker_id,
            retry_count=retry_count,
        )
