import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.user import UserEntity
from tests.conftest import AGENT_UUID

pytestmark = pytest.mark.asyncio


class TestGetNotificationPreferences:
    async def test_user_without_stored_preferences_sees_all_notification_types_enabled(
        self, client: AsyncClient, agent_token: str, db_session: AsyncSession,
    ) -> None:
        result = await db_session.execute(select(UserEntity).where(UserEntity.id == AGENT_UUID))
        agent = result.scalar_one()
        agent.notification_prefs = None
        await db_session.flush()

        response = await client.get(
            "/users/me/notification-preferences",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        for key, value in data.items():
            assert value is True, f"{key} should be True by default"

    async def test_user_sees_their_saved_preferences_when_some_types_are_disabled(
        self, client: AsyncClient, agent_token: str, db_session: AsyncSession,
    ) -> None:
        result = await db_session.execute(select(UserEntity).where(UserEntity.id == AGENT_UUID))
        agent = result.scalar_one()
        agent.notification_prefs = {"deposit_reported": False, "closure_confirmed": False}
        await db_session.flush()

        response = await client.get(
            "/users/me/notification-preferences",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["deposit_reported"] is False
        assert data["closure_confirmed"] is False
        assert data["listing_post_approved"] is True
        assert data["listing_expired"] is True

    async def test_authenticated_user_can_retrieve_their_preferences(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/users/me/notification-preferences",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "listing_post_created" in data
        assert "deposit_reported" in data

    async def test_unauthenticated_user_cannot_retrieve_preferences(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/users/me/notification-preferences")
        assert response.status_code == 401
