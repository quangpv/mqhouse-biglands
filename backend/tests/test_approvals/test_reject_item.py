import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity, ListingStatus
from src.data.entities.notification import NotificationEntity
from tests.conftest import ADMIN_UUID

pytestmark = pytest.mark.asyncio


class TestRejectItem:
    async def test_approver_rejects_listing_post_and_status_returns_to_draft_with_reason(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_approval_listing}/reject",
            json={"reason": "Hình ảnh không rõ ràng"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "REJECTED"
        assert data["listing_status"] == "DRAFT"

    async def test_approver_rejects_deposit_and_listing_stays_in_con_hang(
        self, client: AsyncClient, admin_token: str, pending_deposit_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_deposit_listing}/reject",
            json={"reason": "Chứng từ không hợp lệ"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "REJECTED"
        assert data["listing_status"] == "CON_HANG"

    async def test_reject_without_reason_returns_422(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_approval_listing}/reject",
            json={},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 422

    async def test_double_reject_returns_409(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        await client.post(
            f"/approvals/{pending_approval_listing}/reject",
            json={"reason": "Sai thông tin"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        response = await client.post(
            f"/approvals/{pending_approval_listing}/reject",
            json={"reason": "Lý do khác"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409

    async def test_re_reject_after_new_cycle_succeeds(
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
            f"/approvals/{pending_approval_listing}/reject",
            json={"reason": "Version 1 reject"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["listing_status"] == "DRAFT"

        listing.status = ListingStatus.PENDING_APPROVAL
        listing.approval_version = 2
        await db_session.flush()

        response = await client.post(
            f"/approvals/{pending_approval_listing}/reject",
            json={"reason": "Version 2 reject"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["listing_status"] == "DRAFT"

    async def test_reject_listing_with_no_pending_request_returns_409(
        self, client: AsyncClient, admin_token: str, draft_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{draft_listing}/reject",
            json={"reason": "Không có yêu cầu"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409

    async def test_reject_nonexistent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/approvals/{fake_id}/reject",
            json={"reason": "Lý do hủy"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_admin_can_reject_own_listing(
        self, client: AsyncClient, admin_token: str, pending_admin_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_admin_listing}/reject",
            json={"reason": "Kiểm tra lại thông tin"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "REJECTED"
        assert data["listing_status"] == "DRAFT"

    async def test_approver_cannot_reject_own_listing(
        self, client: AsyncClient, approver_token: str, pending_approver_listing: str,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_approver_listing}/reject",
            json={"reason": "Tự từ chối"},
            headers={"Authorization": f"Bearer {approver_token}"},
        )
        assert response.status_code == 409

    async def test_no_self_notification_when_admin_rejects_own_listing(
        self, client: AsyncClient, admin_token: str, pending_admin_listing: str, db_session: AsyncSession,
    ) -> None:
        response = await client.post(
            f"/approvals/{pending_admin_listing}/reject",
            json={"reason": "Cần chỉnh sửa thêm"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201

        result = await db_session.execute(
            select(func.count(NotificationEntity.id)).where(
                NotificationEntity.user_id == ADMIN_UUID,
                NotificationEntity.event_type == "listing_post_rejected",
            )
        )
        assert result.scalar_one() == 0
