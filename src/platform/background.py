import asyncio
import logging
from collections.abc import Callable, Coroutine
from typing import Any

logger = logging.getLogger("biglands.background")


class BackgroundExecutor:
    def __init__(self, max_retries: int = 3) -> None:
        self._queue: asyncio.Queue[tuple[Callable[..., Coroutine[Any, Any, Any]], dict[str, Any]]] = asyncio.Queue()
        self._max_retries = max_retries

    async def enqueue(self, fn: Callable[..., Coroutine[Any, Any, Any]], **kwargs: Any) -> None:
        await self._queue.put((fn, kwargs))

    async def worker(self) -> None:
        while True:
            fn, kwargs = await self._queue.get()
            for attempt in range(self._max_retries):
                try:
                    await fn(**kwargs)
                    break
                except Exception:
                    logger.exception("Background task failed (attempt %d/%d)", attempt + 1, self._max_retries)
                    if attempt == self._max_retries - 1:
                        logger.error("Background task exhausted retries, discarding")
            self._queue.task_done()

    async def shutdown(self, timeout: float = 5.0) -> None:
        try:
            await asyncio.wait_for(self._queue.join(), timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning("Background executor shutdown timed out after %.1fs", timeout)
