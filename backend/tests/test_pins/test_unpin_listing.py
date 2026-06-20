import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestUnpinListing:
    async def test_agent_unpins_a_previously_pinned_listing(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        await client.put(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        response = await client.delete(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 204

    async def test_agent_can_unpin_a_listing_that_was_never_pinned(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        response = await client.delete(
            f"/listings/{agent_listing}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 204

    async def test_agent_cannot_unpin_a_nonexistent_listing(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.delete(
            f"/listings/{fake_id}/pin",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_unpin_a_listing(
        self, client: AsyncClient, agent_listing: str,
    ) -> None:
        response = await client.delete(f"/listings/{agent_listing}/pin")
        assert response.status_code == 401
