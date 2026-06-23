import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_agent_with_valid_credentials_can_log_in(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_fails_when_username_does_not_exist(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "nonexistent", "password": "admin123"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_fails_when_password_is_incorrect(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_deactivated_account_cannot_log_in(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "deactivated", "password": "deac123"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Account is deactivated"
