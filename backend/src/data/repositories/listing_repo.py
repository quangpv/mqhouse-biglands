import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data.entities.listing import ListingEntity, ListingStatus, TransactionType
from src.platform.config import settings
from src.platform.dependencies import get_db


from src.data.repositories._base import Repo


class ListingRepo(Repo):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, listing_id: uuid.UUID) -> ListingEntity | None:
        result = await self.db.execute(
            select(ListingEntity)
            .options(selectinload(ListingEntity.created_by))
            .where(ListingEntity.id == listing_id)
        )
        return result.scalar_one_or_none()

    async def get_by_ids(self, listing_ids: list[uuid.UUID]) -> list[ListingEntity]:
        result = await self.db.execute(
            select(ListingEntity)
            .options(selectinload(ListingEntity.created_by))
            .where(ListingEntity.id.in_(listing_ids))
        )
        return list(result.scalars().all())

    async def get_with_lock(self, listing_id: uuid.UUID) -> ListingEntity | None:
        result = await self.db.execute(
            select(ListingEntity).where(ListingEntity.id == listing_id).with_for_update()
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> ListingEntity | None:
        result = await self.db.execute(select(ListingEntity).where(ListingEntity.code == code))
        return result.scalar_one_or_none()

    async def create(self, listing: ListingEntity) -> ListingEntity:
        self.db.add(listing)
        await self.db.flush()
        return listing

    async def save(self, listing: ListingEntity) -> ListingEntity:
        self.db.add(listing)
        await self.db.flush()
        await self.db.refresh(listing)
        return listing

    async def hard_delete(self, listing_id: uuid.UUID) -> None:
        listing = await self.get(listing_id)
        if listing:
            await self.db.delete(listing)
            await self.db.flush()

    async def delete(self, listing_id: uuid.UUID) -> None:
        listing = await self.get(listing_id)
        if listing:
            listing.deleted_at = datetime.now(timezone.utc)
            await self.db.flush()

    async def count_active(self) -> int:
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count(ListingEntity.id)).where(ListingEntity.status == ListingStatus.CON_HANG)
        )
        return result.scalar_one()

    async def count_expired(self) -> int:
        from sqlalchemy import func
        cutoff = datetime.now(timezone.utc) - timedelta(days=settings.expiration_days)
        result = await self.db.execute(
            select(func.count(ListingEntity.id)).where(
                ListingEntity.created_at < cutoff,
                ListingEntity.status.in_([ListingStatus.CON_HANG, ListingStatus.PENDING_APPROVAL]),
            )
        )
        return result.scalar_one()

    async def list_expired(self, cutoff: datetime) -> list[ListingEntity]:
        result = await self.db.execute(
            select(ListingEntity).where(
                ListingEntity.created_at < cutoff,
                ListingEntity.status.in_([ListingStatus.CON_HANG, ListingStatus.PENDING_APPROVAL]),
            )
        )
        return list(result.scalars().all())

    async def get_hot_listings(self) -> list[ListingEntity]:
        result = await self.db.execute(
            select(ListingEntity)
            .where(ListingEntity.is_hot.is_(True))
            .order_by(ListingEntity.hot_order.asc().nullslast())
        )
        return list(result.scalars().all())

    async def get_hot_listing_ids(self) -> set[uuid.UUID]:
        result = await self.db.execute(
            select(ListingEntity.id).where(ListingEntity.is_hot.is_(True))
        )
        return {row[0] for row in result}

    async def count_hot_listings(self) -> int:
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count(ListingEntity.id)).where(ListingEntity.is_hot.is_(True))
        )
        return result.scalar_one()

    def build_list_query(
        self,
        search: str | None = None,
        transaction_type: str | None = None,
        status: list[str] | None = None,
        property_type: str | None = None,
        filter_by: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        owner_id: uuid.UUID | None = None,
        is_hot: bool | None = None,
    ):
        query = select(ListingEntity).options(selectinload(ListingEntity.created_by))

        if owner_id:
            query = query.where(ListingEntity.created_by_id == owner_id)
        elif not status:
            query = query.where(ListingEntity.status.in_([ListingStatus.CON_HANG, ListingStatus.DA_COC]))

        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    ListingEntity.code.ilike(pattern),
                    ListingEntity.title.ilike(pattern),
                    ListingEntity.description.ilike(pattern),
                    ListingEntity.address.ilike(pattern),
                )
            )
        if transaction_type:
            query = query.where(ListingEntity.transaction_type == TransactionType(transaction_type))
        if status:
            query = query.where(ListingEntity.status.in_([ListingStatus(s) for s in status]))
        if property_type:
            from src.data.entities.listing import PropertyType
            query = query.where(ListingEntity.property_type == PropertyType(property_type))

        if filter_by == "hot":
            query = query.where(ListingEntity.is_hot.is_(True))
        elif filter_by == "pinned":
            from src.data.entities.user_pin import UserPinEntity
            query = query.join(UserPinEntity, UserPinEntity.listing_id == ListingEntity.id)

        if is_hot is True:
            query = query.where(ListingEntity.is_hot.is_(True))
        elif is_hot is False:
            query = query.where(~ListingEntity.is_hot.is_(True))

        sort_column = {
            "created_at": ListingEntity.created_at,
            "price": ListingEntity.price,
            "view_count": ListingEntity.view_count,
        }.get(sort_by or "created_at", ListingEntity.created_at)

        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        return query
