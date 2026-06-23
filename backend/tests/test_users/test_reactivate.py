import pytest
from httpx import AsyncClient

from tests.conftest import DEACTIVATED_UUID


@pytest.mark.asyncio
async def test_admin_can_reactivate_user(client: AsyncClient, admin_token: str) -> None:
    response = await client.patch(
        f"/users/{DEACTIVATED_UUID}/reactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is True
    assert data["id"] == str(DEACTIVATED_UUID)


@pytest.mark.asyncio
async def test_reactivate_user_without_auth_fails(client: AsyncClient) -> None:
    response = await client.patch(f"/users/{DEACTIVATED_UUID}/reactivate")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_reactivate_nonexistent_user_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.patch(
        "/users/00000000-0000-0000-0000-000000009999/reactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
