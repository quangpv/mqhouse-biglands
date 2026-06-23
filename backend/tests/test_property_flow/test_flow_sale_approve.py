import pytest
from httpx import AsyncClient



@pytest.mark.asyncio
async def test_sale_submit_then_approve(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    submit_resp = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert submit_resp.status_code == 200
    assert submit_resp.json()["status"] == "post_pending"

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    approve_resp = await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": "Approved"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "approved"

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
    assert len(logs) == 2
    assert logs[0]["action"] == "submit"
    assert logs[1]["action"] == "approve"


@pytest.mark.asyncio
async def test_sale_deposit_then_approve(
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

    deposit_resp = await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={"customer_name": "Buyer", "customer_phone": "0900000099",
              "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert deposit_resp.status_code == 200
    assert deposit_resp.json()["status"] == "deposit_pending"

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    approve_resp = await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": "Deposit approved"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert approve_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "deposited"


@pytest.mark.asyncio
async def test_sale_complete_then_approve(
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

    complete_resp = await client.post(
        f"/properties/{prop_id}/transitions/complete",
        json={"customer_name": "Buyer", "customer_phone": "0900000099",
              "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert complete_resp.status_code == 200
    assert complete_resp.json()["status"] == "complete_pending"

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    approve_resp = await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": "Complete approved"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert approve_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_sale_cancel_then_approve(
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

    cancel_resp = await client.post(
        f"/properties/{prop_id}/transitions/cancel",
        json={"notes": "Buyer backed out"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["status"] == "cancel_pending"

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    approve_resp = await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": "Cancel approved"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert approve_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "available"


@pytest.mark.asyncio
async def test_sale_edit_then_approve(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    update_resp = await client.put(
        f"/properties/{prop_id}",
        json={"price": 7000000000, "description": "Updated by sale"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "edit_pending"

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    approve_resp = await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": "Edit approved"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert approve_resp.status_code == 200

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert get_resp.json()["status"] == "available"
    assert get_resp.json()["description"] == "Updated by sale"
