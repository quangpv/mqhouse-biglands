import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_withdraw_property_by_sale(client: AsyncClient, agent_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json={**property_payload, "type": "post_pending"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/withdraw",
        json={"notes": "Changed mind"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_withdraw_property_wrong_status_fails(client: AsyncClient, agent_token: str,
                                                     property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/withdraw",
        json={"notes": None},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_withdraw_property_not_owner_fails(client: AsyncClient, admin_token: str, agent_token: str,
                                                  property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json={**property_payload, "type": "post_pending"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/withdraw",
        json={"notes": None},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_withdraw_property_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/properties/00000000-0000-0000-0000-000000009999/transitions/withdraw",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_withdraw_property_unauthorized(client: AsyncClient) -> None:
    response = await client.post(
        "/properties/00000000-0000-0000-0000-000000009999/transitions/withdraw",
        json={"notes": None},
    )
    assert response.status_code == 401
