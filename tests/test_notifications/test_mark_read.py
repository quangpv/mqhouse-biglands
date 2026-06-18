import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestMarkRead:
    async def test_agent_marks_own_notification_as_read(
        self, client: AsyncClient, agent_token: str, agent_notification: str,
    ) -> None:
        response = await client.patch(
            f"/notifications/{agent_notification}/read",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_read"] is True

    async def test_agent_cannot_mark_another_users_notification(
        self, client: AsyncClient, agent_token: str, admin_notification: str,
    ) -> None:
        response = await client.patch(
            f"/notifications/{admin_notification}/read",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_marking_non_existent_notification_returns_404(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.patch(
            f"/notifications/{fake_id}/read",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_marking_an_already_read_notification_is_harmless(
        self, client: AsyncClient, agent_token: str, agent_notifications: dict,
    ) -> None:
        read_id = agent_notifications["read_ids"][0]
        response = await client.patch(
            f"/notifications/{read_id}/read",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["is_read"] is True

    async def test_unauthenticated_user_cannot_mark_read(
        self, client: AsyncClient, agent_notification: str,
    ) -> None:
        response = await client.patch(f"/notifications/{agent_notification}/read")
        assert response.status_code == 401
