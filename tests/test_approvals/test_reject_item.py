import uuid

import pytest
from httpx import AsyncClient

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
