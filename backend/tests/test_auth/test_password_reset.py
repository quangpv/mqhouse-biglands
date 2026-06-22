import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestPasswordReset:
    async def test_forgot_password_returns_token_for_existing_user(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(
            "/auth/forgot-password",
            json={"username": "admin"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "message" in data

    async def test_forgot_password_returns_error_for_nonexistent_user(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(
            "/auth/forgot-password",
            json={"username": "nonexistent"},
        )
        assert response.status_code == 404

    async def test_reset_password_with_valid_token(
        self, client: AsyncClient,
    ) -> None:
        forgot_resp = await client.post(
            "/auth/forgot-password",
            json={"username": "admin"},
        )
        assert forgot_resp.status_code == 200
        token = forgot_resp.json()["token"]

        response = await client.post(
            "/auth/reset-password",
            json={"token": token, "new_password": "newadmin123"},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Password reset successfully"

        login_resp = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "newadmin123"},
        )
        assert login_resp.status_code == 200
        assert "token" in login_resp.json()

    async def test_reset_password_with_invalid_token_returns_error(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(
            "/auth/reset-password",
            json={"token": "invalid-token", "new_password": "newadmin123"},
        )
        assert response.status_code == 400
