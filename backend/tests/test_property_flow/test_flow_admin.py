import pytest
from httpx import AsyncClient



@pytest.mark.asyncio
async def test_admin_soldout_from_available(
    client: AsyncClient, admin_token: str, property_payload: dict,
) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    assert create_resp.json()["status"] == "draft"

    submit_resp = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert submit_resp.status_code == 200
    assert submit_resp.json()["status"] == "available"

    soldout_resp = await client.post(
        f"/properties/{prop_id}/transitions/soldout",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert soldout_resp.status_code == 200
    assert soldout_resp.json()["status"] == "soldout"

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "soldout"

    logs_resp = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    logs = logs_resp.json()
    assert len(logs) == 2
    assert logs[0]["action"] == "submit"
    assert logs[1]["action"] == "soldout"


@pytest.mark.asyncio
async def test_admin_full_to_completed(
    client: AsyncClient, admin_token: str, property_payload: dict,
) -> None:
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
        json={"customer_name": "Buyer", "customer_phone": "0900000099",
              "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    complete_resp = await client.post(
        f"/properties/{prop_id}/transitions/complete",
        json={"customer_name": "Buyer", "customer_phone": "0900000099",
              "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert complete_resp.status_code == 200
    assert complete_resp.json()["status"] == "completed"

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "completed"

    logs_resp = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    logs = logs_resp.json()
    assert len(logs) == 3
    assert logs[0]["action"] == "submit"
    assert logs[1]["action"] == "deposit"
    assert logs[2]["action"] == "complete"


@pytest.mark.asyncio
async def test_admin_cancel_returns_to_available(
    client: AsyncClient, admin_token: str, property_payload: dict,
) -> None:
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
        json={"customer_name": "Buyer", "customer_phone": "0900000099",
              "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    cancel_resp = await client.post(
        f"/properties/{prop_id}/transitions/cancel",
        json={"notes": "Cancelled"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["status"] == "available"

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "available"

    logs_resp = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    logs = logs_resp.json()
    assert len(logs) == 3
    assert logs[2]["action"] == "cancel"


@pytest.mark.asyncio
async def test_admin_soldout_from_deposited(
    client: AsyncClient, admin_token: str, property_payload: dict,
) -> None:
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
        json={"customer_name": "Buyer", "customer_phone": "0900000099",
              "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    soldout_resp = await client.post(
        f"/properties/{prop_id}/transitions/soldout",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert soldout_resp.status_code == 200
    assert soldout_resp.json()["status"] == "soldout"

    logs_resp = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    logs = logs_resp.json()
    assert len(logs) == 3
    assert logs[2]["action"] == "soldout"


@pytest.mark.asyncio
async def test_admin_update_in_place(
    client: AsyncClient, admin_token: str, property_payload: dict,
) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    update_resp = await client.put(
        f"/properties/{prop_id}",
        json={"price": 7000000000, "description": "Updated description"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["status"] == "available"
    assert data["description"] == "Updated description"
    assert data["price"] == "7.0E+9"

    logs_resp = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    logs = logs_resp.json()
    assert len(logs) == 2
    assert logs[1]["action"] == "edit"
