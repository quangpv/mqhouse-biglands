import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.usefixtures("seed_lookups")


@pytest.mark.asyncio
async def test_edit_pending_has_old_values(
    client: AsyncClient, admin_token: str, edit_pending_approval: tuple,
) -> None:
    _, approval_id = edit_pending_approval
    assert approval_id is not None

    response = await client.get(
        f"/approvals/{approval_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["request"]["old_values"] is not None
    assert "price" in data["request"]["old_values"]
    assert "description" in data["request"]["old_values"]
    assert data["request"]["old_values"]["price"] == 5000000000
    assert data["request"]["old_values"]["description"] == "Approval test property"


@pytest.mark.asyncio
async def test_post_pending_has_no_old_values(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval

    response = await client.get(
        f"/approvals/{approval_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["request"]["old_values"] is None


@pytest.mark.asyncio
async def test_old_values_contains_only_changed_fields(
    client: AsyncClient, admin_token: str, agent_token: str,
    seed_lookups: None, property_payload: dict,
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

    await client.put(
        f"/properties/{prop_id}",
        json={"price": 7000000000},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approval_id = list_resp.json()["data"][0]["id"]

    response = await client.get(
        f"/approvals/{approval_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    data = response.json()
    old = data["request"]["old_values"]
    assert "price" in old
    assert "description" not in old
    assert old["price"] == 5000000000
