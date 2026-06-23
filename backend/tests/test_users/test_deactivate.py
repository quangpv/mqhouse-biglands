import pytest
from httpx import AsyncClient

from tests.conftest import AGENT_UUID


@pytest.mark.asyncio
async def test_admin_can_deactivate_user(client: AsyncClient, admin_token: str) -> None:
    response = await client.patch(
        f"/users/{AGENT_UUID}/deactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is False
    assert data["id"] == str(AGENT_UUID)


@pytest.mark.asyncio
async def test_deactivate_user_without_auth_fails(client: AsyncClient) -> None:
    response = await client.patch(f"/users/{AGENT_UUID}/deactivate")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_deactivate_nonexistent_user_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.patch(
        "/users/00000000-0000-0000-0000-000000009999/deactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
