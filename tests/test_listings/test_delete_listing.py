import uuid

import pytest
from httpx import AsyncClient

from tests.test_listings.conftest import CON_HANG_AGENT_ID

pytestmark = pytest.mark.asyncio


class TestDeleteListing:
    async def test_owner_can_delete_draft_listing(
        self, client: AsyncClient, agent_token: str, agent_draft: str,
    ) -> None:
        response = await client.delete(
            f"/listings/{agent_draft}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 204

    async def test_non_owner_cannot_delete_listing(
        self, client: AsyncClient, agent_token: str, admin_draft: str,
    ) -> None:
        response = await client.delete(
            f"/listings/{admin_draft}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_delete_non_draft_listing_returns_409(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.delete(
            f"/listings/{CON_HANG_AGENT_ID}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409

    async def test_delete_nonexistent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.delete(
            "/listings/00000000-0000-0000-0000-000000000099",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_delete_listing(
        self, client: AsyncClient,
    ) -> None:
        response = await client.delete(f"/listings/{CON_HANG_AGENT_ID}")
        assert response.status_code == 401
