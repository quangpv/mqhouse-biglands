import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestPinListing:
    async def test_agent_pins_a_listing_and_it_shows_as_pinned(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        response = await client.put(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_pinned"] is True
        assert data["id"] == agent_listing

    async def test_agent_can_pin_the_same_listing_multiple_times_without_error(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        response1 = await client.put(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response1.status_code == 200

        response2 = await client.put(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response2.status_code == 200

    async def test_agent_cannot_pin_a_nonexistent_listing(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.put(
            f"/listings/{fake_id}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_pin_a_listing(
        self, client: AsyncClient, agent_listing: str,
    ) -> None:
        response = await client.put(f"/listings/{agent_listing}/pin")
        assert response.status_code == 401
