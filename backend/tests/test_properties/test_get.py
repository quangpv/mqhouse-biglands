import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.usefixtures("seed_lookups")


@pytest.mark.asyncio
async def test_get_property(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == prop_id
    assert data["description"] == "A nice property"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_get_property_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/properties/00000000-0000-0000-0000-000000009999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_property_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/properties/00000000-0000-0000-0000-000000009999")
    assert response.status_code == 401
