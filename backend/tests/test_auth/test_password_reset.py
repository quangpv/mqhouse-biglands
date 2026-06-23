import pytest
from httpx import AsyncClient

from tests.conftest import FakeEmailService

pytestmark = pytest.mark.asyncio


class TestPasswordReset:
    async def test_forgot_password_sends_email_for_existing_user(
        self, client: AsyncClient, override_email_service: None, fake_email_service: FakeEmailService,
    ) -> None:
        response = await client.post(
            "/auth/forgot-password",
            json={"email": "admin@biglands.com"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Password reset link sent to your email"
        assert len(fake_email_service.sent_emails) == 1
        assert fake_email_service.sent_emails[0]["email"] == "admin@biglands.com"
        assert "token" in fake_email_service.sent_emails[0]

    async def test_forgot_password_returns_error_for_nonexistent_user(
        self, client: AsyncClient, override_email_service: None, fake_email_service: FakeEmailService,
    ) -> None:
        response = await client.post(
            "/auth/forgot-password",
            json={"email": "nonexistent@test.com"},
        )
        assert response.status_code == 404
        assert len(fake_email_service.sent_emails) == 0

    async def test_reset_password_with_valid_token(
        self, client: AsyncClient, override_email_service: None, fake_email_service: FakeEmailService,
    ) -> None:
        forgot_resp = await client.post(
            "/auth/forgot-password",
            json={"email": "admin@biglands.com"},
        )
        assert forgot_resp.status_code == 200
        token = fake_email_service.sent_emails[0]["token"]

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
        assert "access_token" in login_resp.json()

    async def test_reset_password_with_invalid_token_returns_error(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(
            "/auth/reset-password",
            json={"token": "invalid-token", "new_password": "newadmin123"},
        )
        assert response.status_code == 400
