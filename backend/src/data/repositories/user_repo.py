import uuid

from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data.entities.user import UserEntity, UserRole
from src.platform.dependencies import get_db


from src.data.repositories._base import Repo


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

    async def count_active_admins(self) -> int:
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count(UserEntity.id)).where(UserEntity.role == UserRole.ADMIN, UserEntity.is_active.is_(True))
        )
        return result.scalar_one()

    async def list_by_role(self, role: UserRole) -> list[UserEntity]:
        result = await self.db.execute(
            select(UserEntity)
            .options(selectinload(UserEntity.organization))
            .where(UserEntity.role == role, UserEntity.is_active.is_(True))
        )
        return list(result.scalars().all())

    async def list_by_roles(self, *roles: UserRole) -> list[UserEntity]:
        result = await self.db.execute(
            select(UserEntity)
            .options(selectinload(UserEntity.organization))
            .where(UserEntity.role.in_(roles), UserEntity.is_active.is_(True))
        )
        return list(result.scalars().all())

    async def list_by_ids(self, ids: list[uuid.UUID]) -> list[UserEntity]:
        result = await self.db.execute(
            select(UserEntity)
            .options(selectinload(UserEntity.organization))
            .where(UserEntity.id.in_(ids))
        )
        return list(result.scalars().all())

    async def create(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        await self.db.flush()
        return user

    async def save(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    def build_list_query(self, search: str | None = None, role: str | None = None, is_active: bool | None = None):
        query = select(UserEntity).options(selectinload(UserEntity.organization))
        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    UserEntity.full_name.ilike(pattern),
                    UserEntity.username.ilike(pattern),
                    UserEntity.phone.ilike(pattern),
                )
            )
        if role:
            query = query.where(UserEntity.role == UserRole(role))
        if is_active is not None:
            query = query.where(UserEntity.is_active.is_(is_active))
        query = query.order_by(UserEntity.created_at.desc())
        return query
