import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_agent_with_valid_credentials_can_log_in(client: AsyncClient) -> None:
        """An active agent with valid username and password receives a JWT token."""
        response = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_fails_when_username_does_not_exist(client: AsyncClient) -> None:
        """A login attempt with a username that isn't registered is rejected.
        The error message does not reveal whether the username or password was wrong."""
        response = await client.post(
            "/auth/login",
            json={"username": "nonexistent", "password": "admin123"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_login_fails_when_password_is_incorrect(client: AsyncClient) -> None:
        """A login attempt with a valid username but wrong password is rejected.
        The error message is identical to the 'user not found' case to prevent username enumeration."""
        response = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_deactivated_account_cannot_log_in(client: AsyncClient) -> None:
        """A user whose account has been deactivated cannot log in, even with valid credentials."""
        response = await client.post(
            "/auth/login",
            json={"username": "deactivated", "password": "deac123"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Account is deactivated"
