import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListUsers:
    async def test_admin_can_view_paginated_list_of_all_users(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/users",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) >= 3
        assert data["page"] == 1
        assert data["size"] == 20

    async def test_admin_can_search_users_by_name(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/users",
            params={"search": "Admin"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert all("Admin" in u["full_name"] for u in data)

    async def test_admin_can_search_users_by_username(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/users",
            params={"search": "agent"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert all("agent" in u["username"] for u in data)

    async def test_admin_can_filter_users_by_role(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/users",
            params={"role": "AGENT"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert all(u["role"] == "AGENT" for u in data)

    async def test_admin_can_filter_inactive_users(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/users",
            params={"is_active": "false"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert all(u["is_active"] is False for u in data)
        assert len(data) >= 1

    async def test_listing_users_is_only_allowed_for_admins(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/users",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
