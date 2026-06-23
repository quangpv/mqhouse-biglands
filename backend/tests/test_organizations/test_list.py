import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_list_organizations(client: AsyncClient, admin_token: str) -> None:
    resp1 = await client.post(
        "/organizations/",
        json={
            "name": "list-org-a",
            "display_name": "Org A",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    resp2 = await client.post(
        "/organizations/",
        json={
            "name": "list-org-b",
            "display_name": "Org B",
            "transaction_types": [],
            "property_types": [],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        "/organizations/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    names = [item["name"] for item in data]
    assert "list-org-a" in names
    assert "list-org-b" in names


@pytest.mark.asyncio
async def test_list_organizations_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get("/organizations/")
    assert response.status_code == 401
