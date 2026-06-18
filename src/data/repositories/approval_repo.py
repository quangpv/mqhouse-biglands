import uuid

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.approval import ApprovalEntity, ApprovalType
from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingEntity, ListingStatus
from src.platform.dependencies import get_db


class ApprovalRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_queue_counts(self) -> list[dict]:
        counts: list[dict] = []

        result = await self.db.execute(
            select(ListingEntity.transaction_type, func.count(ListingEntity.id))
            .where(ListingEntity.status == ListingStatus.PENDING_APPROVAL)
            .group_by(ListingEntity.transaction_type)
        )
        for row in result:
            counts.append({
                "approval_type": ApprovalType.LISTING_POST,
                "transaction_type": row[0],
                "count": row[1],
            })

        event_approval_map = [
            (DealEventType.DEPOSIT_REPORTED, ApprovalType.DEPOSIT),
            (DealEventType.CLOSURE_REPORTED, ApprovalType.CLOSURE),
            (DealEventType.CANCELLATION_REPORTED, ApprovalType.CANCELLATION),
            (DealEventType.SOLD_OUT_REPORTED, ApprovalType.SOLD_OUT),
        ]

        for event_type, approval_type in event_approval_map:
            result = await self.db.execute(
                select(ListingEntity.transaction_type, func.count(DealEventEntity.id))
                .join(ListingEntity, DealEventEntity.listing_id == ListingEntity.id)
                .where(
                    DealEventEntity.event_type == event_type,
                    DealEventEntity.confirmed_by_id.is_(None),
                )
                .group_by(ListingEntity.transaction_type)
            )
            for row in result:
                counts.append({
                    "approval_type": approval_type,
                    "transaction_type": row[0],
                    "count": row[1],
                })

        return counts

    async def list_listing_post_queue_items(
        self,
        transaction_type: str | None = None,
    ) -> list[dict]:
        query = select(ListingEntity).where(ListingEntity.status == ListingStatus.PENDING_APPROVAL)
        if transaction_type:
            from src.data.entities.listing import TransactionType
            query = query.where(ListingEntity.transaction_type == TransactionType(transaction_type))
        query = query.order_by(ListingEntity.created_at.desc())
        result = await self.db.execute(query)
        listings = result.scalars().all()
        return [
            {
                "id": l.id,
                "listing_id": l.id,
                "listing_code": l.code,
                "listing": l,
                "approval_type": ApprovalType.LISTING_POST,
                "transaction_type": l.transaction_type,
                "title": l.title,
                "price": l.price,
                "status": l.status,
                "created_at": l.created_at,
            }
            for l in listings
        ]

    async def list_deal_event_queue_items(
        self,
        approval_type: ApprovalType,
        transaction_type: str | None = None,
    ) -> list[dict]:
        event_type_map = {
            ApprovalType.DEPOSIT: DealEventType.DEPOSIT_REPORTED,
            ApprovalType.CLOSURE: DealEventType.CLOSURE_REPORTED,
            ApprovalType.CANCELLATION: DealEventType.CANCELLATION_REPORTED,
            ApprovalType.SOLD_OUT: DealEventType.SOLD_OUT_REPORTED,
        }
        event_type = event_type_map[approval_type]

        query = (
            select(ListingEntity, DealEventEntity)
            .join(DealEventEntity, DealEventEntity.listing_id == ListingEntity.id)
            .where(
                DealEventEntity.event_type == event_type,
                DealEventEntity.confirmed_by_id.is_(None),
            )
        )
        if transaction_type:
            from src.data.entities.listing import TransactionType
            query = query.where(ListingEntity.transaction_type == TransactionType(transaction_type))
        query = query.order_by(DealEventEntity.created_at.desc())
        result = await self.db.execute(query)
        rows = result.all()

        items = []
        for listing, event in rows:
            items.append({
                "id": event.listing_id,
                "listing_id": event.listing_id,
                "listing_code": listing.code,
                "listing": listing,
                "deal_event": event,
                "approval_type": approval_type,
                "transaction_type": listing.transaction_type,
                "title": listing.title,
                "price": listing.price,
                "status": listing.status,
                "created_at": event.created_at,
                "customer_name": event.customer_name,
                "customer_phone": event.customer_phone,
                "deposit_amount": event.deposit_amount,
                "event_notes": event.notes,
            })
        return items

    async def get_pending_listing_post(self, listing_id: uuid.UUID) -> dict | None:
        result = await self.db.execute(
            select(ListingEntity).where(
                ListingEntity.id == listing_id,
                ListingEntity.status == ListingStatus.PENDING_APPROVAL,
            )
        )
        listing = result.scalar_one_or_none()
        if listing is None:
            return None
        return {
            "id": listing.id,
            "listing_id": listing.id,
            "listing_code": listing.code,
            "listing": listing,
            "approval_type": ApprovalType.LISTING_POST,
            "transaction_type": listing.transaction_type,
            "title": listing.title,
            "price": listing.price,
            "status": listing.status,
            "created_at": listing.created_at,
        }

    async def get_pending_deal_event_by_listing(
        self, listing_id: uuid.UUID
    ) -> dict | None:
        listing_result = await self.db.execute(
            select(ListingEntity).where(ListingEntity.id == listing_id)
        )
        listing = listing_result.scalar_one_or_none()
        if listing is None:
            return None

        event_approval_map = [
            (DealEventType.DEPOSIT_REPORTED, ApprovalType.DEPOSIT),
            (DealEventType.CLOSURE_REPORTED, ApprovalType.CLOSURE),
            (DealEventType.CANCELLATION_REPORTED, ApprovalType.CANCELLATION),
            (DealEventType.SOLD_OUT_REPORTED, ApprovalType.SOLD_OUT),
        ]

        for event_type, approval_type in event_approval_map:
            result = await self.db.execute(
                select(DealEventEntity).where(
                    DealEventEntity.listing_id == listing_id,
                    DealEventEntity.event_type == event_type,
                    DealEventEntity.confirmed_by_id.is_(None),
                )
            )
            event = result.scalar_one_or_none()
            if event is not None:
                return {
                    "id": listing.id,
                    "listing_id": listing.id,
                    "listing_code": listing.code,
                    "listing": listing,
                    "deal_event": event,
                    "approval_type": approval_type,
                    "transaction_type": listing.transaction_type,
                    "title": listing.title,
                    "price": listing.price,
                    "status": listing.status,
                    "created_at": event.created_at,
                    "customer_name": event.customer_name,
                    "customer_phone": event.customer_phone,
                    "deposit_amount": event.deposit_amount,
                    "event_notes": event.notes,
                }

        return None

    async def get_approval_by_listing_and_type(
        self, listing_id: uuid.UUID, approval_type: ApprovalType
    ) -> ApprovalEntity | None:
        result = await self.db.execute(
            select(ApprovalEntity).where(
                ApprovalEntity.listing_id == listing_id,
                ApprovalEntity.approval_type == approval_type,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, approval: ApprovalEntity) -> ApprovalEntity:
        self.db.add(approval)
        await self.db.flush()
        return approval
