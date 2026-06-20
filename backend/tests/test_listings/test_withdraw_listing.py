import uuid

import pytest
from httpx import AsyncClient

from tests.test_listings.conftest import CON_HANG_ADMIN_ID, DRAFT_ADMIN_ID

pytestmark = pytest.mark.asyncio


class TestWithdrawListing:
    async def test_owner_can_withdraw_CON_HANG_listing_to_draft(
        self, client: AsyncClient, agent_token: str, agent_con_hang: str,
    ) -> None:
        response = await client.post(
            f"/listings/{agent_con_hang}/withdraw",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "DRAFT"

    async def test_owner_can_withdraw_PENDING_APPROVAL_listing_to_draft(
        self, client: AsyncClient, agent_token: str, agent_pending: str,
    ) -> None:
        response = await client.post(
            f"/listings/{agent_pending}/withdraw",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "DRAFT"

    async def test_non_owner_cannot_withdraw_listing(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            f"/listings/{CON_HANG_ADMIN_ID}/withdraw",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_withdraw_draft_listing_returns_409(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            f"/listings/{DRAFT_ADMIN_ID}/withdraw",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409

    async def test_withdraw_nonexistent_listing_returns_404(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/listings/{fake_id}/withdraw",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_withdraw_listing(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(f"/listings/{CON_HANG_ADMIN_ID}/withdraw")
        assert response.status_code == 401
