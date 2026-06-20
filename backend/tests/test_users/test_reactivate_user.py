import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import AGENT_UUID, DEACTIVATED_UUID

pytestmark = pytest.mark.asyncio


class TestReactivateUser:
    async def test_admin_can_reactivate_a_deactivated_user(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{DEACTIVATED_UUID}/reactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is True
        assert data["id"] == str(DEACTIVATED_UUID)

    async def test_reactivating_an_already_active_user_succeeds(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{AGENT_UUID}/reactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["is_active"] is True

    async def test_reactivating_a_non_existent_user_returns_not_found(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.patch(
            f"/users/{fake_id}/reactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_reactivating_users_is_only_allowed_for_admins(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{DEACTIVATED_UUID}/reactivate",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
