import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListOrganizations:
    async def test_admin_can_list_all_organizations(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/organizations",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) >= 2
        names = [org["display_name"] for org in data["data"]]
        assert "MQ Land" in names
        assert "ID Land" in names

    async def test_agent_can_list_all_organizations(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/organizations",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200

    async def test_unauthenticated_user_cannot_list_organizations(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/organizations")
        assert response.status_code == 401

    async def test_list_organizations_returns_paginated_response(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/organizations?page=1&size=10",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "page" in data
        assert "size" in data
        assert "total" in data
        assert "total_pages" in data
