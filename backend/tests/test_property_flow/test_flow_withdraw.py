import pytest
from httpx import AsyncClient



@pytest.mark.asyncio
async def test_withdraw_from_post_pending(
    client: AsyncClient, agent_token: str, admin_token: str, property_payload: dict,
) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    submit_resp = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": "Submit for review"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert submit_resp.status_code == 200
    assert submit_resp.json()["status"] == "post_pending"

    withdraw_resp = await client.post(
        f"/properties/{prop_id}/transitions/withdraw",
        json={"notes": "Changed mind"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert withdraw_resp.status_code == 200
    assert withdraw_resp.json()["status"] == "draft"

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert get_resp.json()["status"] == "draft"

    logs_resp = await client.get(
        f"/properties/{prop_id}/status-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    logs = logs_resp.json()
    assert len(logs) == 2
    assert logs[0]["action"] == "submit"
    assert logs[1]["action"] == "withdraw"


@pytest.mark.asyncio
async def test_withdraw_from_edit_pending_fails(
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

    await client.put(
        f"/properties/{prop_id}",
        json={"price": 7000000000},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    withdraw_resp = await client.post(
        f"/properties/{prop_id}/transitions/withdraw",
        json={"notes": None},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert withdraw_resp.status_code == 403
