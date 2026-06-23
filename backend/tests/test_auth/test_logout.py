import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_any_authenticated_user_can_log_out(client: AsyncClient, admin_token: str) -> None:
        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logged out successfully"


@pytest.mark.asyncio
async def test_logged_out_token_cannot_be_used_again(client: AsyncClient, admin_token: str) -> None:
        await client.post("/auth/logout", headers={"Authorization": f"Bearer {admin_token}"})
        response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Token has been revoked"
