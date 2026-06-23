import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_create_organization(client: AsyncClient, admin_token: str) -> None:
    tx_resp = await client.post(
        "/transaction-types/",
        json={"code": "ORG_TX", "display_name": "Org Tx"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    tx_id = tx_resp.json()["id"]

    response = await client.post(
        "/organizations/",
        json={
            "name": "test-org",
            "display_name": "Test Organization",
            "transaction_types": [tx_id],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test-org"
    assert data["display_name"] == "Test Organization"
    assert data["transaction_types"] == [tx_id]
    assert data["property_types"] == []
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_non_admin_cannot_create_organization(client: AsyncClient, agent_token: str) -> None:
    response = await client.post(
        "/organizations/",
        json={
            "name": "no-perm",
            "display_name": "No Perm",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_organization_without_auth_fails(client: AsyncClient) -> None:
    response = await client.post(
        "/organizations/",
        json={
            "name": "no-auth",
            "display_name": "No Auth",
            "transaction_types": [],
            "property_types": [],
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_organization_with_duplicate_name_returns_409(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/organizations/",
        json={
            "name": "dup-org",
            "display_name": "Original",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.post(
        "/organizations/",
        json={
            "name": "dup-org",
            "display_name": "Duplicate",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
