import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity, ListingStatus
from src.data.entities.notification import NotificationEntity
from tests.conftest import ADMIN_UUID

pytestmark = pytest.mark.asyncio


class TestApproveItem:
    async def test_approver_approves_listing_post_and_status_becomes_con_hang(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_approval_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "APPROVED"
        assert data["listing_status"] == "CON_HANG"
        assert data["listing_code"] is not None

    async def test_approver_approves_deposit_and_status_becomes_da_coc(
        self, client: AsyncClient, admin_token: str, pending_deposit_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_deposit_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "APPROVED"
        assert data["listing_status"] == "DA_COC"

    async def test_approver_approves_closure_and_status_becomes_da_chot(
        self, client: AsyncClient, admin_token: str, pending_closure_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_closure_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "APPROVED"
        assert data["listing_status"] == "DA_CHOT"

    async def test_approver_approves_cancellation_and_status_returns_to_con_hang(
        self, client: AsyncClient, admin_token: str, pending_cancellation_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_cancellation_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "APPROVED"
        assert data["listing_status"] == "CON_HANG"

    async def test_approver_approves_sold_out_and_status_becomes_het_hang(
        self, client: AsyncClient, admin_token: str, pending_sold_out_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_sold_out_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "APPROVED"
        assert data["listing_status"] == "HET_HANG"

    async def test_double_approve_returns_409(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        await client.post(
            f"/approvals/{pending_approval_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        response = await client.post(
            f"/approvals/{pending_approval_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409

    async def test_re_approve_after_new_cycle_succeeds(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str, db_session: AsyncSession,
    ) -> None:
        listing_id = uuid.UUID(pending_approval_listing)
        result = await db_session.execute(
            select(ListingEntity).where(ListingEntity.id == listing_id)
        )
        listing = result.scalar_one()
        listing.approval_version = 1
        await db_session.flush()

        response = await client.post(
            f"/approvals/{pending_approval_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["listing_status"] == "CON_HANG"

        listing.status = ListingStatus.PENDING_APPROVAL
        listing.approval_version = 2
        await db_session.flush()

        response = await client.post(
            f"/approvals/{pending_approval_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["listing_status"] == "CON_HANG"

    async def test_approve_listing_with_no_pending_request_returns_409(
        self, client: AsyncClient, admin_token: str, draft_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{draft_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409

    async def test_approve_nonexistent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/approvals/{fake_id}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_admin_can_approve_own_listing(
        self, client: AsyncClient, admin_token: str, pending_admin_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_admin_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "APPROVED"
        assert data["listing_status"] == "CON_HANG"

    async def test_approver_cannot_approve_own_listing(
        self, client: AsyncClient, approver_token: str, pending_approver_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_approver_listing}/approve",
            headers={"Authorization": f"Bearer {approver_token}"},
        )
        assert response.status_code == 409

    async def test_no_self_notification_when_admin_approves_own_listing(
        self, client: AsyncClient, admin_token: str, pending_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_admin_listing}/approve",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201

        result = await db_session.execute(
            select(func.count(NotificationEntity.id)).where(
                NotificationEntity.user_id == ADMIN_UUID,
                NotificationEntity.event_type == "listing_post_approved",
            )
        )
        assert result.scalar_one() == 0
