import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_list_users(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "metadata" in data
    assert len(data["data"]) >= 4
    usernames = [u["username"] for u in data["data"]]
    assert "admin" in usernames
    assert "agent" in usernames
    for u in data["data"]:
        assert "property_type_ids" in u
        assert "transaction_type_ids" in u


@pytest.mark.asyncio
async def test_list_users_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get("/users/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_users_filter_by_role(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/users/?role=SALE",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    for u in data["data"]:
        assert u["role"] == "SALE"


@pytest.mark.asyncio
async def test_list_users_filter_by_is_active(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/users/?is_active=false",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    for u in data["data"]:
        assert u["is_active"] is False


@pytest.mark.asyncio
async def test_list_users_search_by_name(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/users/?search=Admin",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 1
    assert data["data"][0]["full_name"] == "Admin User"


@pytest.mark.asyncio
async def test_list_users_pagination(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/users/?page=1&size=2",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) <= 2
    assert data["metadata"]["page"] == 1
    assert data["metadata"]["size"] == 2
    assert data["metadata"]["total_pages"] >= 1
