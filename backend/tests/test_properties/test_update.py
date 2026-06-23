import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_update_property_by_admin(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.put(
        f"/properties/{prop_id}",
        json={"title": "Updated Title", "description": "Updated description"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_update_property_by_sale_owner(client: AsyncClient, agent_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.put(
        f"/properties/{prop_id}",
        json={"title": "Sale Updated"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Sale Updated"
    assert data["status"] == "edit_pending"
    assert data["requires_approval"] is True


@pytest.mark.asyncio
async def test_update_property_not_owner_fails(client: AsyncClient, agent_token: str, admin_token: str,
                                                property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.put(
        f"/properties/{prop_id}",
        json={"title": "Hacked"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_property_wrong_status_fails(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json={**property_payload, "type": "post_pending"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.put(
        f"/properties/{prop_id}",
        json={"title": "Should Fail"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200

    create_deposited = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    dep_id = create_deposited.json()["id"]
    await client.post(
        f"/properties/{dep_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    await client.post(
        f"/properties/{dep_id}/transitions/deposit",
        json={"customer_name": "Buyer", "customer_phone": "0900000099", "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.put(
        f"/properties/{dep_id}",
        json={"title": "Should Also Fail"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_property_unauthorized(client: AsyncClient, property_payload: dict) -> None:
    response = await client.put("/properties/00000000-0000-0000-0000-000000009999", json={"title": "x"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_property_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        "/properties/00000000-0000-0000-0000-000000009999",
        json={"title": "x"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
