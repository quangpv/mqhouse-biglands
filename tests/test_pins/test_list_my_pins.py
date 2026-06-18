import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListMyPins:
    async def test_agent_sees_pinned_listing_in_personal_list(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        await client.put(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        response = await client.get(
            "/users/me/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == agent_listing
        assert data["data"][0]["is_pinned"] is True

    async def test_agent_sees_empty_list_when_nothing_is_pinned(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/users/me/pins",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    async def test_pinned_listings_are_per_user(
        self, client: AsyncClient, agent_token: str, admin_token: str, agent_listing: str,
    ) -> None:
        await client.put(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        response = await client.get(
            "/users/me/pins",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    async def test_unauthenticated_user_cannot_list_pins(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/users/me/pins")
        assert response.status_code == 401
