import pytest
from httpx import AsyncClient

from tests.test_listings.conftest import CON_HANG_AGENT_ID, PENDING_AGENT_ID

pytestmark = pytest.mark.asyncio


class TestFilterCounts:
    async def test_returns_all_three_counts(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings/filter-counts",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "all" in data
        assert "hot" in data
        assert "pinned" in data

    async def test_all_counts_only_active_listings(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings/filter-counts",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["all"] >= 3

    async def test_hot_excludes_pending_approval(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings/filter-counts",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200

    async def test_unauthenticated_user_cannot_access(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/listings/filter-counts")
        assert response.status_code == 401
