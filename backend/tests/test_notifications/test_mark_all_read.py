import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestMarkAllRead:
    async def test_mark_all_sets_all_agent_notifications_to_read(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        response = await client.post(
            "/notifications/read-all",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["updated"] == 2

        count_response = await client.get(
            "/notifications/unread-count",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert count_response.json()["count"] == 0

    async def test_only_the_users_notifications_are_affected(
        self, client: AsyncClient, agent_token: str, admin_token: str,
        agent_notifications: dict, admin_notification: str,
    ) -> None:
        await client.post(
            "/notifications/read-all",
            headers={"Authorization": f"Bearer {agent_token}"},
        )

        admin_count = await client.get(
            "/notifications/unread-count",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert admin_count.json()["count"] == 1

    async def test_mark_all_when_none_unread_is_harmless(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        await client.post(
            "/notifications/read-all",
            headers={"Authorization": f"Bearer {agent_token}"},
        )

        response = await client.post(
            "/notifications/read-all",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["updated"] == 0

    async def test_unauthenticated_user_cannot_mark_all_read(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post("/notifications/read-all")
        assert response.status_code == 401
