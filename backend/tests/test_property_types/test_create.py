import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_create_property_type(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/property-types/",
        json={"code": "NHA_O", "display_name": "Nhà ở"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "NHA_O"
    assert data["display_name"] == "Nhà ở"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_non_admin_cannot_create_property_type(client: AsyncClient, agent_token: str) -> None:
    response = await client.post(
        "/property-types/",
        json={"code": "CAN_HO", "display_name": "Căn hộ"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_property_type_without_auth_fails(client: AsyncClient) -> None:
    response = await client.post(
        "/property-types/",
        json={"code": "DAT_NEN", "display_name": "Đất nền"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_property_type_with_duplicate_code_returns_409(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/property-types/",
        json={"code": "DUPE_TYPE", "display_name": "Original"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.post(
        "/property-types/",
        json={"code": "DUPE_TYPE", "display_name": "Duplicate"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
