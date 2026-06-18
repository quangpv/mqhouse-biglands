import uuid

import pytest
from httpx import AsyncClient

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
