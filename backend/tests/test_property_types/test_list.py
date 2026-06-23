import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_list_property_types(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/property-types/",
        json={"code": "NHA_O", "display_name": "Nhà ở"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        "/property-types/",
        json={"code": "CAN_HO", "display_name": "Căn hộ"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        "/property-types/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    codes = [item["code"] for item in data]
    assert "NHA_O" in codes
    assert "CAN_HO" in codes


@pytest.mark.asyncio
async def test_list_property_types_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get("/property-types/")
    assert response.status_code == 401
