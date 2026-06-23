import pytest
from httpx import AsyncClient

from tests.conftest import AGENT_UUID


@pytest.mark.asyncio
async def test_admin_can_update_user(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        f"/users/{AGENT_UUID}",
        json={"full_name": "Updated Agent"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Agent"
    assert data["username"] == "agent"


@pytest.mark.asyncio
async def test_admin_can_update_user_role(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        f"/users/{AGENT_UUID}",
        json={"role": "APPROVER"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "APPROVER"


@pytest.mark.asyncio
async def test_admin_can_update_user_type_ids(client: AsyncClient, admin_token: str) -> None:
    tx_resp = await client.post(
        "/transaction-types/",
        json={"code": "UPD_TX", "display_name": "Update Tx"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    tx_id = tx_resp.json()["id"]

    pt_resp = await client.post(
        "/property-types/",
        json={"code": "UPD_PT", "display_name": "Update Pt"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    pt_id = pt_resp.json()["id"]

    response = await client.put(
        f"/users/{AGENT_UUID}",
        json={"property_type_ids": [pt_id], "transaction_type_ids": [tx_id]},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["property_type_ids"] == [pt_id]
    assert data["transaction_type_ids"] == [tx_id]


@pytest.mark.asyncio
async def test_update_user_without_auth_fails(client: AsyncClient) -> None:
    response = await client.put(
        f"/users/{AGENT_UUID}",
        json={"full_name": "No Auth"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_user_non_admin_returns_403(client: AsyncClient, agent_token: str) -> None:
    response = await client.put(
        f"/users/{AGENT_UUID}",
        json={"full_name": "Agent Trying"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_user_duplicate_email_returns_409(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        f"/users/{AGENT_UUID}",
        json={"email": "admin@biglands.com"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_nonexistent_user_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        "/users/00000000-0000-0000-0000-000000009999",
        json={"full_name": "Ghost"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_cannot_demote_self(client: AsyncClient, admin_token: str) -> None:
    from tests.conftest import ADMIN_UUID

    response = await client.put(
        f"/users/{ADMIN_UUID}",
        json={"role": "SALE"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403
