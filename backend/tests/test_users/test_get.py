import pytest
from httpx import AsyncClient

from tests.conftest import AGENT_UUID


@pytest.mark.asyncio
async def test_admin_can_get_user(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        f"/users/{AGENT_UUID}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(AGENT_UUID)
    assert data["username"] == "agent"
    assert data["full_name"] == "Agent User"
    assert "property_type_ids" in data
    assert "transaction_type_ids" in data


@pytest.mark.asyncio
async def test_get_user_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get(f"/users/{AGENT_UUID}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/users/00000000-0000-0000-0000-000000009999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
