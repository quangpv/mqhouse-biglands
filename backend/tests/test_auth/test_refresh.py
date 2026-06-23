import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestRefreshToken:
    async def test_user_can_refresh_access_token(self, client: AsyncClient) -> None:
        login_resp = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert login_resp.status_code == 200
        refresh_token = login_resp.json()["refresh_token"]

        refresh_resp = await client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_resp.status_code == 200
        data = refresh_resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["refresh_token"] != refresh_token

    async def test_refresh_with_revoked_token_is_rejected(self, client: AsyncClient) -> None:
        login_resp = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert login_resp.status_code == 200
        refresh_token = login_resp.json()["refresh_token"]

        resp1 = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert resp1.status_code == 200

        resp2 = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert resp2.status_code == 401
        assert resp2.json()["message"] == "Refresh token has been revoked"

    async def test_refresh_with_invalid_token_is_rejected(self, client: AsyncClient) -> None:
        response = await client.post(
            "/auth/refresh",
            json={"refresh_token": "some-invalid-token"},
        )
        assert response.status_code == 401
