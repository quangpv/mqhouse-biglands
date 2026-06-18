import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestGetUnreadCount:
    async def test_agent_sees_correct_unread_count(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        response = await client.get(
            "/notifications/unread-count",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["count"] == 2

    async def test_admin_sees_their_own_unread_count(
        self, client: AsyncClient, admin_token: str, admin_notification: str,
    ) -> None:
        response = await client.get(
            "/notifications/unread-count",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["count"] == 1

    async def test_reading_a_notification_decreases_unread_count(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        unread_id = agent_notifications["unread_ids"][0]
        await client.patch(
            f"/notifications/{unread_id}/read",
            headers={"Authorization": f"Bearer {agent_token}"},
        )

        response = await client.get(
            "/notifications/unread-count",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.json()["count"] == 1

    async def test_zero_unread_returns_zero(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        for nid in agent_notifications["unread_ids"]:
            await client.patch(
                f"/notifications/{nid}/read",
                headers={"Authorization": f"Bearer {agent_token}"},
            )

        response = await client.get(
            "/notifications/unread-count",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.json()["count"] == 0

    async def test_unauthenticated_user_cannot_get_unread_count(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/notifications/unread-count")
        assert response.status_code == 401
