import uuid

from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data.entities.user import UserEntity, UserRole
from src.data.repositories._base import Repo
from src.platform.dependencies import get_db

_USER_LOADS = [
    selectinload(UserEntity.organization),
    selectinload(UserEntity.transaction_types),
    selectinload(UserEntity.property_types),
]


class UserRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def search(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
        search: str | None = None,
        organization_id: uuid.UUID | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[UserEntity], int]:
        query = select(UserEntity).options(*_USER_LOADS)

        if role is not None:
            query = query.where(UserEntity.role == role)
        if is_active is not None:
            query = query.where(UserEntity.is_active == is_active)
        if organization_id is not None:
            query = query.where(UserEntity.organization_id == organization_id)
        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    UserEntity.full_name.ilike(pattern),
                    UserEntity.username.ilike(pattern),
                    UserEntity.email.ilike(pattern),
                    UserEntity.phone.ilike(pattern),
                )
            )

        query = query.order_by(UserEntity.created_at.desc())
        return await self.paginated_list(query, page=page, size=size)

    async def get(self, user_id: uuid.UUID) -> UserEntity | None:
        result = await self.db.execute(
            select(UserEntity)
            .options(*_USER_LOADS)
            .where(UserEntity.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> UserEntity | None:
        result = await self.db.execute(
            select(UserEntity)
            .options(*_USER_LOADS)
            .where(UserEntity.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> UserEntity | None:
        result = await self.db.execute(
            select(UserEntity)
            .options(*_USER_LOADS)
            .where(UserEntity.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_organization(self, organization_id: uuid.UUID) -> list[UserEntity]:
        result = await self.db.execute(
            select(UserEntity)
            .options(*_USER_LOADS)
            .where(UserEntity.organization_id == organization_id)
        )
        return list(result.scalars().all())

    async def save(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
