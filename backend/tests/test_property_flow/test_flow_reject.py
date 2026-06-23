import pytest
from httpx import AsyncClient



@pytest.mark.asyncio
async def test_reject_submit_returns_to_draft(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    reject_resp = await client.post(
        f"/approvals/{approval_id}/reject",
        json={"reason": "Incomplete info"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reject_resp.status_code == 200
    assert reject_resp.json()["status"] == "rejected"

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "draft"

    logs_resp = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    logs = logs_resp.json()
    assert len(logs) == 2
    assert logs[1]["action"] == "reject"


@pytest.mark.asyncio
async def test_reject_deposit_returns_to_available(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
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
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    reject_resp = await client.post(
        f"/approvals/{approval_id}/reject",
        json={"reason": "Deposit rejected"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reject_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "available"


@pytest.mark.asyncio
async def test_reject_cancel_returns_to_deposited(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
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

    await client.post(
        f"/properties/{prop_id}/transitions/cancel",
        json={"notes": "Buyer backed out"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    reject_resp = await client.post(
        f"/approvals/{approval_id}/reject",
        json={"reason": "Cancel rejected"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reject_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "deposited"


@pytest.mark.asyncio
async def test_reject_complete_returns_to_deposited(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
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

    await client.post(
        f"/properties/{prop_id}/transitions/complete",
        json={"customer_name": "Buyer", "customer_phone": "0900000099",
              "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    reject_resp = await client.post(
        f"/approvals/{approval_id}/reject",
        json={"reason": "Complete rejected"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reject_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "deposited"


@pytest.mark.asyncio
async def test_reject_soldout_returns_to_deposited(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
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

    await client.post(
        f"/properties/{prop_id}/transitions/soldout",
        json={"notes": None},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    reject_resp = await client.post(
        f"/approvals/{approval_id}/reject",
        json={"reason": "Soldout rejected"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reject_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "deposited"
