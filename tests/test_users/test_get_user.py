import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import ADMIN_UUID, AGENT_UUID

pytestmark = pytest.mark.asyncio


class TestGetUser:
    async def test_admin_can_view_details_of_a_specific_user(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            f"/users/{ADMIN_UUID}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(ADMIN_UUID)
        assert data["full_name"] == "Admin User"
        assert data["username"] == "admin"
        assert data["role"] == "ADMIN"
        assert "created_at" in data
        assert "updated_at" in data

    async def test_admin_can_view_another_users_details(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            f"/users/{AGENT_UUID}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(AGENT_UUID)
        assert data["full_name"] == "Agent User"

    async def test_looking_up_a_non_existent_user_returns_not_found(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.get(
            f"/users/{fake_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_viewing_user_details_is_only_allowed_for_admins(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            f"/users/{ADMIN_UUID}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
