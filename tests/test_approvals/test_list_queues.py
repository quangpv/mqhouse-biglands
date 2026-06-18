import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListQueues:
    async def test_approver_lists_all_approval_queues_with_pending_counts(
        self, client: AsyncClient, admin_token: str, pending_approval_listing: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "queues" in data
        assert len(data["queues"]) == 15
        listing_post_queues = [q for q in data["queues"] if q["approval_type"] == "LISTING_POST"]
        assert any(q["count"] > 0 for q in listing_post_queues)

    async def test_queues_include_zero_count_entries(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        zero_count = [q for q in data["queues"] if q["count"] == 0]
        assert len(zero_count) > 0

    async def test_agent_cannot_list_approval_queues(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/approvals/queues",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_unauthenticated_user_cannot_list_queues(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/approvals/queues")
        assert response.status_code == 401
