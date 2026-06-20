import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestGetApproval:
    async def test_approver_views_approval_detail_for_pending_listing_post(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.get(
            f"/approvals/{pending_approval_listing}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["listing_id"] == pending_approval_listing
        assert data["approval_type"] == "LISTING_POST"

    async def test_approver_views_approval_detail_for_pending_deposit(
        self, client: AsyncClient, admin_token: str, pending_deposit_listing: str,
    ) -> None:
        response = await client.get(
            f"/approvals/{pending_deposit_listing}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["approval_type"] == "DEPOSIT"
        assert data["customer_name"] is not None

    async def test_no_pending_approval_returns_404(
        self, client: AsyncClient, admin_token: str, draft_listing: str,
    ) -> None:
        response = await client.get(
            f"/approvals/{draft_listing}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_approval_for_nonexistent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.get(
            f"/approvals/{fake_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
