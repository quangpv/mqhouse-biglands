import pytest
from httpx import AsyncClient

from tests.conftest import AGENT_UUID

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
        assert data["data"][0].get("deal_event") is None
        assert data["data"][0].get("reported_by") is None

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
        deposit_item = next(item for item in data["data"] if item["approval_type"] == "DEPOSIT")
        assert deposit_item["deal_event"] is not None
        assert deposit_item["deal_event"]["event_type"] == "DEPOSIT_REPORTED"
        assert deposit_item["reported_by"] is not None
        assert "full_name" in deposit_item["reported_by"]
        assert "email" in deposit_item["reported_by"]

    async def test_listing_post_queue_can_be_filtered_by_agent_id(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues/LISTING_POST",
            params={"agentId": str(AGENT_UUID)},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1

    async def test_listing_post_queue_filters_by_unknown_agent_returns_empty(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues/LISTING_POST",
            params={"agentId": "00000000-0000-0000-0000-000000009999"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    async def test_listing_post_queue_can_be_filtered_by_date_from(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues/LISTING_POST",
            params={"dateFrom": "2020-01-01T00:00:00"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1

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
