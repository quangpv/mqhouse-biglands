import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_view_their_profile(
    client: AsyncClient,
    admin_token: str,
) -> None:
    response = await client.get(
        "/me",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Admin User"
    assert data["username"] == "admin"
    assert data["role"] == "ADMIN"
    assert data["is_active"] is True
    assert "device_limit_enabled" in data
    assert "property_type_ids" in data
    assert "transaction_type_ids" in data
    assert "organization_name" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_profile_without_token_fails(client: AsyncClient) -> None:
    response = await client.get("/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_with_garbage_token_fails(client: AsyncClient) -> None:
    response = await client.get(
        "/me",
        headers={"Authorization": "Bearer garbage"},
    )
    assert response.status_code == 401
