import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.user import UserEntity
from tests.conftest import AGENT_UUID

pytestmark = pytest.mark.asyncio


class TestUpdateNotificationPreferences:
    async def test_user_can_disable_a_specific_notification_type(
        self, client: AsyncClient, agent_token: str, db_session: AsyncSession,
    ) -> None:
        result = await db_session.execute(select(UserEntity).where(UserEntity.id == AGENT_UUID))
        agent = result.scalar_one()
        agent.notification_prefs = None
        await db_session.flush()

        response = await client.put(
            "/users/me/notification-preferences",
            json={"deposit_reported": False},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["deposit_reported"] is False
        assert data["listing_post_approved"] is True
        assert data["listing_expired"] is True

    async def test_user_can_re_enable_a_previously_disabled_type(
        self, client: AsyncClient, agent_token: str, db_session: AsyncSession,
    ) -> None:
        result = await db_session.execute(select(UserEntity).where(UserEntity.id == AGENT_UUID))
        agent = result.scalar_one()
        agent.notification_prefs = {"deposit_reported": False}
        await db_session.flush()

        response = await client.put(
            "/users/me/notification-preferences",
            json={"deposit_reported": True},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["deposit_reported"] is True

    async def test_updated_preferences_persist_across_subsequent_get(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        put_response = await client.put(
            "/users/me/notification-preferences",
            json={"cancellation_reported": False, "sold_out_confirmed": False},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert put_response.status_code == 200

        get_response = await client.get(
            "/users/me/notification-preferences",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["cancellation_reported"] is False
        assert data["sold_out_confirmed"] is False
        assert data["listing_post_approved"] is True

    async def test_invalid_field_value_returns_validation_error(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.put(
            "/users/me/notification-preferences",
            json={"deposit_reported": "not_a_boolean"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 422

    async def test_unauthenticated_user_cannot_update_preferences(
        self, client: AsyncClient,
    ) -> None:
        response = await client.put(
            "/users/me/notification-preferences",
            json={"deposit_reported": False},
        )
        assert response.status_code == 401
