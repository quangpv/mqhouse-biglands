from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.platform.background import BackgroundExecutor
from src.platform.database import get_session
from src.platform.logger import AppLogger


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


def get_logger() -> AppLogger:
    return Depends(lambda: AppLogger("biglands"))


def get_executor() -> BackgroundExecutor:
    return Depends(lambda: BackgroundExecutor())


def get_scheduler():
    from src.platform.scheduler import AppScheduler
    return Depends(lambda: AppScheduler())
