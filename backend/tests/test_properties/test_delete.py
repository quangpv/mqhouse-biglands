import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_delete_property_draft(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.delete(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_property_soft_delete(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={"customer_name": "Buyer", "customer_phone": "0900000099", "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.delete(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_property_not_owner_fails(client: AsyncClient, admin_token: str, agent_token: str,
                                                property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.delete(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_property_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.delete(
        "/properties/00000000-0000-0000-0000-000000009999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_property_unauthorized(client: AsyncClient) -> None:
    response = await client.delete("/properties/00000000-0000-0000-0000-000000009999")
    assert response.status_code == 401
