import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.organization import OrganizationEntity
from src.data.repositories._base import Repo
from src.platform.dependencies import get_db


class OrganizationRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, org_id: uuid.UUID) -> OrganizationEntity | None:
        result = await self.db.execute(select(OrganizationEntity).where(OrganizationEntity.id == org_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> OrganizationEntity | None:
        result = await self.db.execute(select(OrganizationEntity).where(OrganizationEntity.name == name))
        return result.scalar_one_or_none()

    async def list_all(self) -> list[OrganizationEntity]:
        result = await self.db.execute(select(OrganizationEntity).order_by(OrganizationEntity.display_name))
        return list(result.scalars().all())

    async def create(self, org: OrganizationEntity) -> OrganizationEntity:
        self.db.add(org)
        await self.db.flush()
        return org

    async def save(self, org: OrganizationEntity) -> OrganizationEntity:
        self.db.add(org)
        await self.db.flush()
        await self.db.refresh(org)
        return org

    async def delete(self, org_id: uuid.UUID) -> None:
        org = await self.get(org_id)
        if org:
            await self.db.delete(org)
            await self.db.flush()
