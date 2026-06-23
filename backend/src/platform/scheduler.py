from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI



class AppScheduler:
    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self._scheduler.start()

    def stop(self) -> None:
        self._scheduler.shutdown(wait=False)

    def add_job(self, fn, trigger: str = "interval", **kwargs) -> None:
        self._scheduler.add_job(fn, trigger, **kwargs)


def module(app: FastAPI):
    scheduler = AppScheduler()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        scheduler.start()
        yield
        scheduler.stop()

    app.router.lifespan_context = lifespan
