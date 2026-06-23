import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_update_organization(client: AsyncClient, admin_token: str) -> None:
    tx_resp = await client.post(
        "/transaction-types/",
        json={"code": "UPD_TX", "display_name": "Upd Tx"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    tx_id = tx_resp.json()["id"]

    create_resp = await client.post(
        "/organizations/",
        json={
            "name": "update-org",
            "display_name": "Old Name",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    org_id = create_resp.json()["id"]

    response = await client.put(
        f"/organizations/{org_id}",
        json={
            "name": "updated-org",
            "display_name": "New Name",
            "transaction_types": [tx_id],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated-org"
    assert data["display_name"] == "New Name"
    assert tx_id in data["transaction_types"]


@pytest.mark.asyncio
async def test_non_admin_cannot_update_organization(client: AsyncClient, admin_token: str, agent_token: str) -> None:
    create_resp = await client.post(
        "/organizations/",
        json={
            "name": "update-no-perm",
            "display_name": "No Perm",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    org_id = create_resp.json()["id"]

    response = await client.put(
        f"/organizations/{org_id}",
        json={
            "name": "hacked",
            "display_name": "Hacked",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_nonexistent_organization_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.put(
        f"/organizations/{uuid.uuid4()}",
        json={
            "name": "nope",
            "display_name": "Nope",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_organization_with_duplicate_name_returns_409(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/organizations/",
        json={
            "name": "existing-org",
            "display_name": "Existing",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    create_resp = await client.post(
        "/organizations/",
        json={
            "name": "to-update",
            "display_name": "To Update",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    org_id = create_resp.json()["id"]

    response = await client.put(
        f"/organizations/{org_id}",
        json={
            "name": "existing-org",
            "display_name": "Conflict",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
