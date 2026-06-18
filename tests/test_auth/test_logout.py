import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_any_authenticated_user_can_log_out(client: AsyncClient) -> None:
        """Any user can successfully end their session by calling logout.
        Logout is stateless and always succeeds regardless of authentication state."""
        response = await client.post("/auth/logout")
        assert response.status_code == 204
