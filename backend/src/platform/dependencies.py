from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.platform.database import get_session
from src.platform.email import SmtpEmailService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


def get_email_service() -> SmtpEmailService:
    return SmtpEmailService()
