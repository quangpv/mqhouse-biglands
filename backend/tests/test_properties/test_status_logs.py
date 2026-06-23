import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_get_status_logs_returns_transitions(client: AsyncClient, admin_token: str,
                                                    property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": "First submit"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    last = data[-1]
    assert last["action"] == "submit"
    assert last["to_status"] == "available"
    assert last["notes"] == "First submit"


@pytest.mark.asyncio
async def test_get_status_logs_multiple_transitions(client: AsyncClient, admin_token: str,
                                                     property_payload: dict) -> None:
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
    await client.post(
        f"/properties/{prop_id}/transitions/cancel",
        json={"notes": "Cancelled"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["action"] == "submit"
    assert data[1]["action"] == "deposit"
    assert data[2]["action"] == "cancel"


@pytest.mark.asyncio
async def test_get_status_logs_empty_for_new_property(client: AsyncClient, admin_token: str,
                                                       property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_status_logs_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/properties/00000000-0000-0000-0000-000000009999/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_status_logs_unauthorized(client: AsyncClient) -> None:
    response = await client.get(
        "/properties/00000000-0000-0000-0000-000000009999/status-logs",
    )
    assert response.status_code == 401
