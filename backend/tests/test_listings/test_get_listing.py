import pytest
from httpx import AsyncClient

from tests.test_listings.conftest import CON_HANG_AGENT_ID, SEED_IMAGE_ID

pytestmark = pytest.mark.asyncio


class TestGetListing:
    async def test_get_listing_returns_detail_with_related_data(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            f"/listings/{CON_HANG_AGENT_ID}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(CON_HANG_AGENT_ID)
        assert data["status"] == "CON_HANG"
        assert "images" in data
        assert "deal_events" in data
        assert "is_pinned" in data

    async def test_viewing_listing_increments_view_count(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        r1 = await client.get(
            f"/listings/{CON_HANG_AGENT_ID}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        v1 = r1.json()["view_count"]
        r2 = await client.get(
            f"/listings/{CON_HANG_AGENT_ID}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        v2 = r2.json()["view_count"]
        assert v2 == v1 + 1

    async def test_get_nonexistent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings/00000000-0000-0000-0000-000000000099",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_get_listing(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get(f"/listings/{CON_HANG_AGENT_ID}")
        assert response.status_code == 401
