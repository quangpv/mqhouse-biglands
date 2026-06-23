import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_counts_returns_pending_by_type(
    client: AsyncClient, admin_token: str, agent_token: str, property_payload: dict,
) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": "test"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    response = await client.get(
        "/approvals/counts",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    sell = next((c for c in data if c["transaction_type_code"] == "SELL"), None)
    assert sell is not None
    assert sell["count"] >= 1


@pytest.mark.asyncio
async def test_counts_excludes_approved(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    await client.post(
        f"/approvals/{approval_id}/approve",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        "/approvals/counts",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    sell = next((c for c in data if c["transaction_type_code"] == "SELL"), None)
    if sell:
        assert sell["count"] == 0


@pytest.mark.asyncio
async def test_counts_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get("/approvals/counts")
    assert response.status_code == 401
