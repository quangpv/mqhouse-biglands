"""Seed the database with initial data."""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.organization import (
    OrganizationEntity,
    OrgPropertyTypeEntity,
    OrgTransactionTypeEntity,
)
from src.data.entities.property_type import PropertyTypeEntity
from src.data.entities.transaction_type import TransactionTypeEntity
from src.data.entities.user import UserEntity, UserRole
from src.platform.database import async_session_factory
from src.platform.security import hash_password


_PROPERTY_TYPES = [
    ("apartment", "Chung Cư"),
    ("land", "Nhà Đất"),
    ("rental", "Nhà Trọ"),
]

_TRANSACTION_TYPES = [
    ("sell", "Bán"),
    ("lease", "Cho Thuê"),
]


async def seed() -> None:
    async with async_session_factory() as session:
        await _seed_admin(session)
        await _seed_organization(session)
        await session.commit()


async def _seed_admin(session: AsyncSession) -> None:
    repo = _UserRepo(session)
    existing = await repo.get_by_username("admin")
    if existing:
        print("Admin user already exists, skipping.")
        return

    admin = UserEntity(
        full_name="System Admin",
        username="admin",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    session.add(admin)
    await session.flush()
    print(f"Created admin user: id={admin.id}, username=admin, password=admin123")


async def _seed_organization(session: AsyncSession) -> None:
    result = await session.execute(
        select(OrganizationEntity).where(OrganizationEntity.name == "mqhouse")
    )
    org = result.scalar_one_or_none()
    if org:
        print("Organization MQhouse already exists, skipping.")
        return

    org = OrganizationEntity(name="mqhouse", display_name="MQ House")
    session.add(org)
    await session.flush()

    for code, display_name in _PROPERTY_TYPES:
        pt = await _get_or_create(session, PropertyTypeEntity, code=code, display_name=display_name)
        session.add(OrgPropertyTypeEntity(organization_id=org.id, property_type_id=pt.id))

    for code, display_name in _TRANSACTION_TYPES:
        tt = await _get_or_create(session, TransactionTypeEntity, code=code, display_name=display_name)
        session.add(OrgTransactionTypeEntity(organization_id=org.id, transaction_type_id=tt.id))

    print("Seeded organization MQhouse with property types and transaction types.")


async def _get_or_create(session: AsyncSession, model, **kwargs):
    filters = [getattr(model, k) == v for k, v in kwargs.items()]
    result = await session.execute(select(model).where(*filters))
    instance = result.scalar_one_or_none()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    await session.flush()
    return instance


class _UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> UserEntity | None:
        result = await self.db.execute(
            select(UserEntity).where(UserEntity.username == username)
        )
        return result.scalar_one_or_none()


if __name__ == "__main__":
    asyncio.run(seed())
