import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_logged_in_user_can_see_their_own_profile(client: AsyncClient, admin_token: str) -> None:
        """An authenticated user can retrieve their profile information
        including username, role, and account status."""
        response = await client.get(
            "/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["role"] == "ADMIN"
        assert data["is_active"] is True

@pytest.mark.asyncio
async def test_unauthenticated_request_is_rejected(client: AsyncClient) -> None:
        """Requests to a protected endpoint without an authentication token
        are rejected with a 401 status code."""
        response = await client.get("/me")
        assert response.status_code == 401
        assert response.json()["message"] == "Missing authorization header"

@pytest.mark.asyncio
async def test_request_with_expired_or_invalid_token_is_rejected(client: AsyncClient) -> None:
        """Requests with a malformed, expired, or otherwise invalid token
        are rejected to protect against unauthorized access."""
        response = await client.get(
            "/me",
            headers={"Authorization": "Bearer invalidtoken"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Invalid or expired token"
