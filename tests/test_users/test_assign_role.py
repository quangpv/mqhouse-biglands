import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import ADMIN_UUID, AGENT_UUID

pytestmark = pytest.mark.asyncio


class TestAssignRole:
    async def test_admin_can_promote_an_agent_to_approver(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{AGENT_UUID}/role",
            json={"role": "APPROVER"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "APPROVER"
        assert data["id"] == str(AGENT_UUID)

    async def test_admin_can_promote_a_user_to_admin(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{AGENT_UUID}/role",
            json={"role": "ADMIN"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["role"] == "ADMIN"

    async def test_admin_cannot_change_role_of_the_last_admin(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{ADMIN_UUID}/role",
            json={"role": "AGENT"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409
        assert "last active admin" in response.json()["detail"].lower()

    async def test_admin_can_change_role_when_another_admin_exists(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        resp = await client.post(
            "/users",
            json={
                "full_name": "Second Admin",
                "username": "secondadmin",
                "password": "secret123",
                "role": "ADMIN",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        admin2_id = resp.json()["id"]

        response = await client.patch(
            f"/users/{ADMIN_UUID}/role",
            json={"role": "APPROVER"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["role"] == "APPROVER"

    async def test_assigning_an_invalid_role_returns_validation_error(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{AGENT_UUID}/role",
            json={"role": "INVALID"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 422

    async def test_assigning_roles_is_only_allowed_for_admins(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.patch(
            f"/users/{AGENT_UUID}/role",
            json={"role": "APPROVER"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
