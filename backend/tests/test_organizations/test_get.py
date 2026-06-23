import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_get_organization(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    tx_resp = await client.post(
        "/transaction-types/",
        json={"code": "GET_TX", "display_name": "Get Tx"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    tx_id = tx_resp.json()["id"]

    create_resp = await client.post(
        "/organizations/",
        json={
            "name": "get-org",
            "display_name": "Get Org",
            "transaction_types": [tx_id],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    org_id = create_resp.json()["id"]

    response = await client.get(
        f"/organizations/{org_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "get-org"
    assert data["display_name"] == "Get Org"
    assert tx_id in data["transaction_types"]


@pytest.mark.asyncio
async def test_get_nonexistent_organization_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        f"/organizations/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_organization_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get(f"/organizations/{uuid.uuid4()}")
    assert response.status_code == 401
