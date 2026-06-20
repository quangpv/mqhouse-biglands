import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

NEW_USER = {
    "full_name": "Nguyễn Văn A",
    "username": "nguyenvana",
    "password": "secret123",
}


class TestCreateUserAccount:
    async def test_admin_can_create_an_agent_user_with_full_name_and_login_credentials(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            "/users",
            json=NEW_USER,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == "Nguyễn Văn A"
        assert data["username"] == "nguyenvana"
        assert data["role"] == "AGENT"
        assert data["is_active"] is True

    async def test_admin_can_create_a_user_with_optional_phone_number(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        payload = {**NEW_USER, "username": "withphone", "phone": "0909123456"}
        response = await client.post(
            "/users",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["phone"] == "0909123456"

    async def test_admin_can_create_a_user_with_approver_role(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        payload = {**NEW_USER, "username": "approver1", "role": "APPROVER"}
        response = await client.post(
            "/users",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["role"] == "APPROVER"

    async def test_admin_can_create_another_admin_user(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        payload = {**NEW_USER, "username": "admin2", "role": "ADMIN"}
        response = await client.post(
            "/users",
            json=payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        assert response.json()["role"] == "ADMIN"

    async def test_admin_cannot_create_a_user_with_a_duplicate_username(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        await client.post(
            "/users",
            json=NEW_USER,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        response = await client.post(
            "/users",
            json=NEW_USER,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Username already exists"

    async def test_creating_users_is_only_allowed_for_admins(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            "/users",
            json=NEW_USER,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
