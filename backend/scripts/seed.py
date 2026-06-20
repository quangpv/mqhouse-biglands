"""Seed the database with an initial admin user."""

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.user import UserEntity, UserRole
from src.platform.database import async_session_factory
from src.platform.security import hash_password


async def seed() -> None:
    async with async_session_factory() as session:
        repo = _UserRepo(session)
        existing = await repo.get_by_username("admin")
        if existing:
            print("Admin user already exists, skipping seed.")
            return

        admin = UserEntity(
            full_name="System Admin",
            username="admin",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        print(f"Created admin user: id={admin.id}, username=admin, password=admin123")


class _UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> UserEntity | None:
        from sqlalchemy import select
        result = await self.db.execute(select(UserEntity).where(UserEntity.username == username))
        return result.scalar_one_or_none()


if __name__ == "__main__":
    asyncio.run(seed())
