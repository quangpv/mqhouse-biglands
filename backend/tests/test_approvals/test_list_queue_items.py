import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListQueueItems:
    async def test_approver_lists_items_in_listing_post_queue(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues/LISTING_POST",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        assert data["data"][0]["approval_type"] == "LISTING_POST"

    async def test_invalid_queue_type_returns_400(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues/INVALID_TYPE",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    async def test_approver_lists_items_in_deposit_queue(
        self, client: AsyncClient, admin_token: str, pending_deposit_listing: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues/DEPOSIT",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert any(item["approval_type"] == "DEPOSIT" for item in data["data"])

    async def test_agent_cannot_list_queue_items(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues/LISTING_POST",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_unauthenticated_user_cannot_list_queue_items(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/approvals/queues/LISTING_POST")
        assert response.status_code == 401
