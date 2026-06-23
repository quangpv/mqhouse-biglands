import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestChangePassword:
    async def test_user_can_change_password_with_valid_current_password(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            "/auth/change-password",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"current_password": "admin123", "new_password": "newpass456"},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Password changed successfully"

        login_resp = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "newpass456"},
        )
        assert login_resp.status_code == 200
        assert "access_token" in login_resp.json()

    async def test_change_password_fails_with_wrong_current_password(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            "/auth/change-password",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"current_password": "wrongpassword", "new_password": "newpass456"},
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Current password is incorrect"

    async def test_change_password_requires_authentication(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(
            "/auth/change-password",
            json={"current_password": "admin123", "new_password": "newpass456"},
        )
        assert response.status_code == 401
