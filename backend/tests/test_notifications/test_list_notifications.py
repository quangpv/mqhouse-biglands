import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListNotifications:
    async def test_agent_sees_their_own_notifications_with_correct_structure(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        response = await client.get(
            "/notifications",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3
        assert data["total"] == 3
        assert data["page"] == 1
        assert data["size"] == 20
        assert "total_pages" in data
        first = data["data"][0]
        assert "id" in first
        assert "user_id" in first
        assert "title" in first
        assert "body" in first
        assert "reference_type" in first
        assert "reference_id" in first
        assert "is_read" in first
        assert "created_at" in first

    async def test_agent_does_not_see_other_users_notifications(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict, admin_notification: str,
    ) -> None:
        response = await client.get(
            "/notifications",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        for item in data["data"]:
            assert item["id"] != admin_notification

    async def test_notifications_can_be_filtered_by_read_status(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        response = await client.get(
            "/notifications?is_read=true",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert all(item["is_read"] is True for item in data["data"])

        response = await client.get(
            "/notifications?is_read=false",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert all(item["is_read"] is False for item in data["data"])

    async def test_pagination_params_reduce_returned_count(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        response = await client.get(
            "/notifications?per_page=2",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2
        assert data["total"] == 3

    async def test_unauthenticated_user_cannot_list_notifications(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/notifications")
        assert response.status_code == 401
