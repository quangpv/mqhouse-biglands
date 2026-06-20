import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import ADMIN_UUID, AGENT_UUID, DEACTIVATED_UUID

pytestmark = pytest.mark.asyncio


class TestDeactivateUser:
    async def test_admin_can_deactivate_an_active_user(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{AGENT_UUID}/deactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
        assert data["id"] == str(AGENT_UUID)

    async def test_admin_cannot_deactivate_their_own_account(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{ADMIN_UUID}/deactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Cannot deactivate yourself"

    async def test_admin_cannot_deactivate_the_last_active_admin(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        payload = {
            "full_name": "Temp Admin",
            "username": "tempadmin",
            "password": "secret123",
            "role": "ADMIN",
        }
        resp = await client.post(
            "/users",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        admin2_id = resp.json()["id"]

        resp = await client.patch(
            f"/users/{admin2_id}/deactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200

        resp = await client.patch(
            f"/users/{admin2_id}/deactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 409
        assert "last active admin" in resp.json()["detail"].lower()

    async def test_deactivating_an_already_inactive_user_succeeds(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{DEACTIVATED_UUID}/deactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["is_active"] is False

    async def test_deactivating_a_non_existent_user_returns_not_found(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.patch(
            f"/users/{fake_id}/deactivate",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_deactivating_users_is_only_allowed_for_admins(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{AGENT_UUID}/deactivate",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
