import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.approval import ApprovalEntity, DecisionType
from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingEntity, ListingStatus

pytestmark = pytest.mark.asyncio


class TestAdminAutoApprove:
    async def test_admin_reports_deposit_on_own_listing_auto_approves(
        self, client: AsyncClient, admin_token: str, con_hang_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = con_hang_admin_listing
        response = await client.post(
            f"/listings/{listing_id}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "DEPOSIT_REPORTED"
        assert data["listing_id"] == listing_id

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.status == ListingStatus.DA_COC

        events = await db_session.execute(
            select(DealEventEntity)
            .where(DealEventEntity.listing_id == uuid.UUID(listing_id))
            .order_by(DealEventEntity.created_at)
        )
        all_events = list(events.scalars().all())
        assert len(all_events) == 2
        assert all_events[0].event_type == DealEventType.DEPOSIT_REPORTED
        assert all_events[1].event_type == DealEventType.DEPOSIT_CONFIRMED
        assert all_events[1].confirmed_by_id is not None

    async def test_admin_reports_deposit_on_agent_listing_auto_approves(
        self, client: AsyncClient, admin_token: str, con_hang_agent_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = con_hang_agent_listing
        response = await client.post(
            f"/listings/{listing_id}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "200000000"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "DEPOSIT_REPORTED"

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.status == ListingStatus.DA_COC

    async def test_admin_reports_closure_auto_approves(
        self, client: AsyncClient, admin_token: str, da_coc_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = da_coc_admin_listing
        response = await client.post(
            f"/listings/{listing_id}/deal-events/closure",
            json={"notes": "Khách đã thanh toán đủ"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "CLOSURE_REPORTED"

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.status == ListingStatus.DA_CHOT

    async def test_admin_reports_cancellation_auto_approves(
        self, client: AsyncClient, admin_token: str, da_coc_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = da_coc_admin_listing
        response = await client.post(
            f"/listings/{listing_id}/deal-events/cancellation",
            json={"notes": "Khách thay đổi ý định"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "CANCELLATION_REPORTED"

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.status == ListingStatus.CON_HANG

    async def test_admin_reports_sold_out_auto_approves(
        self, client: AsyncClient, admin_token: str, con_hang_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = con_hang_admin_listing
        response = await client.post(
            f"/listings/{listing_id}/deal-events/sold-out",
            json={"notes": "Đã bán hết"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "SOLD_OUT_REPORTED"

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.status == ListingStatus.HET_HANG

    async def test_admin_auto_approve_creates_approval_record(
        self, client: AsyncClient, admin_token: str, con_hang_agent_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = con_hang_agent_listing
        await client.post(
            f"/listings/{listing_id}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        result = await db_session.execute(
            select(ApprovalEntity)
            .where(ApprovalEntity.listing_id == uuid.UUID(listing_id))
        )
        approval = result.scalar_one_or_none()
        assert approval is not None
        assert approval.decision == DecisionType.APPROVED

    async def test_agent_reports_deposit_still_creates_pending_event(
        self, client: AsyncClient, agent_token: str, con_hang_agent_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = con_hang_agent_listing
        response = await client.post(
            f"/listings/{listing_id}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "DEPOSIT_REPORTED"

        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == uuid.UUID(listing_id))
        )
        listing = result.scalar_one()
        assert listing.status == ListingStatus.CON_HANG

        events = await db_session.execute(
            select(DealEventEntity)
            .where(
                DealEventEntity.listing_id == uuid.UUID(listing_id),
                DealEventEntity.event_type == DealEventType.DEPOSIT_REPORTED,
            )
        )
        event = events.scalar_one_or_none()
        assert event is not None
        assert event.confirmed_by_id is None

    async def test_admin_auto_approve_preserves_deposit_fields(
        self, client: AsyncClient, admin_token: str, con_hang_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = con_hang_admin_listing
        await client.post(
            f"/listings/{listing_id}/deal-events/deposit",
            json={
                "customer_name": "Trần Thị B",
                "customer_phone": "0987654321",
                "deposit_amount": "300000000",
                "notes": "Khách đã xem nhà",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        events = await db_session.execute(
            select(DealEventEntity)
            .where(DealEventEntity.listing_id == uuid.UUID(listing_id))
            .order_by(DealEventEntity.created_at)
        )
        all_events = list(events.scalars().all())
        confirmed = all_events[1]
        assert confirmed.customer_name == "Trần Thị B"
        assert confirmed.customer_phone == "0987654321"
        assert confirmed.deposit_amount == 300000000
        assert confirmed.notes == "Khách đã xem nhà"

    async def test_admin_auto_approve_marks_reported_event_confirmed(
        self, client: AsyncClient, admin_token: str, con_hang_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = con_hang_admin_listing
        await client.post(
            f"/listings/{listing_id}/deal-events/deposit",
            json={"customer_name": "Nguyễn Văn A", "deposit_amount": "100000000"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        events = await db_session.execute(
            select(DealEventEntity)
            .where(DealEventEntity.listing_id == uuid.UUID(listing_id))
            .order_by(DealEventEntity.created_at)
        )
        all_events = list(events.scalars().all())
        reported = all_events[0]
        assert reported.event_type == DealEventType.DEPOSIT_REPORTED
        assert reported.confirmed_by_id is not None
        assert reported.confirmed_at is not None
