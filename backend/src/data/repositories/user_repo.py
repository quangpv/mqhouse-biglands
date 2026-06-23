import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data.entities.user import UserEntity
from src.data.repositories._base import Repo
from src.platform.dependencies import get_db


class UserRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, user_id: uuid.UUID) -> UserEntity | None:
        result = await self.db.execute(
            select(UserEntity)
            .options(selectinload(UserEntity.organization))
            .where(UserEntity.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> UserEntity | None:
        result = await self.db.execute(
            select(UserEntity)
            .options(selectinload(UserEntity.organization))
            .where(UserEntity.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> UserEntity | None:
        result = await self.db.execute(
            select(UserEntity)
            .options(selectinload(UserEntity.organization))
            .where(UserEntity.email == email)
        )
        return result.scalar_one_or_none()

    async def save(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
