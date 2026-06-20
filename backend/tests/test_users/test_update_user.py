import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import AGENT_UUID

pytestmark = pytest.mark.asyncio


class TestUpdateUser:
    async def test_admin_can_update_a_users_full_name(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.put(
            f"/users/{AGENT_UUID}",
            json={"full_name": "Updated Agent Name"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Agent Name"
        assert data["username"] == "agent"
        assert data["id"] == str(AGENT_UUID)

    async def test_admin_can_update_a_users_phone_and_email(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.put(
            f"/users/{AGENT_UUID}",
            json={"phone": "0999999999", "email": "agent@example.com"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "0999999999"
        assert data["email"] == "agent@example.com"

    async def test_admin_can_update_a_user_with_only_email(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.put(
            f"/users/{AGENT_UUID}",
            json={"email": "newemail@test.com"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "newemail@test.com"

    async def test_updating_a_non_existent_user_returns_not_found(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.put(
            f"/users/{fake_id}",
            json={"full_name": "Nobody"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_updating_users_is_only_allowed_for_admins(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.put(
            f"/users/{AGENT_UUID}",
            json={"full_name": "Hacker"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
