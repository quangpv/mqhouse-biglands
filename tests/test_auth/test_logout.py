import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_any_authenticated_user_can_log_out(client: AsyncClient, admin_token: str) -> None:
        """Any authenticated user can successfully end their session by calling logout."""
        response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204
