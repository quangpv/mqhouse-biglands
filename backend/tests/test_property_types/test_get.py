import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_view_property_type_by_id(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    create_resp = await client.post(
        "/property-types/",
        json={"code": "NHA_O", "display_name": "Nhà ở"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.get(
        f"/property-types/{type_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "NHA_O"
    assert data["display_name"] == "Nhà ở"


@pytest.mark.asyncio
async def test_view_nonexistent_property_type_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        f"/property-types/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_view_property_type_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get(f"/property-types/{uuid.uuid4()}")
    assert response.status_code == 401
