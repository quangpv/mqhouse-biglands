import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_update_property_type(client: AsyncClient, admin_token: str) -> None:
    create_resp = await client.post(
        "/property-types/",
        json={"code": "OLD_TYPE", "display_name": "Old Name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.put(
        f"/property-types/{type_id}",
        json={"code": "NEW_TYPE", "display_name": "New Name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "NEW_TYPE"
    assert data["display_name"] == "New Name"


@pytest.mark.asyncio
async def test_non_admin_cannot_update_property_type(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    create_resp = await client.post(
        "/property-types/",
        json={"code": "UPDATE_ME", "display_name": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.put(
        f"/property-types/{type_id}",
        json={"code": "HACKED", "display_name": "Hacked"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_nonexistent_property_type_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        f"/property-types/{uuid.uuid4()}",
        json={"code": "NOPE", "display_name": "Nope"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_property_type_with_duplicate_code_returns_409(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/property-types/",
        json={"code": "EXISTING", "display_name": "Existing"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    create_resp = await client.post(
        "/property-types/",
        json={"code": "TO_UPDATE", "display_name": "To Update"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    type_id = create_resp.json()["id"]

    response = await client.put(
        f"/property-types/{type_id}",
        json={"code": "EXISTING", "display_name": "Conflict"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
