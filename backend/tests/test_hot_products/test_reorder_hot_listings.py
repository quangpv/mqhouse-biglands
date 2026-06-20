import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestReorderHotListings:
    async def test_admin_reorders_hot_listings(
        self, client: AsyncClient, admin_token: str, hot_listings: list[str],
    ) -> None:
        reversed_ids = list(reversed(hot_listings))
        response = await client.put(
            "/hot-listings/reorder",
            json={"listing_ids": reversed_ids},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        for idx, item in enumerate(data):
            assert item["hot_order"] == idx + 1
        assert data[0]["id"] == hot_listings[2]
        assert data[1]["id"] == hot_listings[1]
        assert data[2]["id"] == hot_listings[0]

    async def test_reorder_with_non_hot_listing_id_returns_400(
        self, client: AsyncClient, admin_token: str, hot_listings: list[str], con_hang_listing: str,
    ) -> None:
        bad_ids = [hot_listings[0], con_hang_listing]
        response = await client.put(
            "/hot-listings/reorder",
            json={"listing_ids": bad_ids},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    async def test_reorder_with_duplicate_ids_returns_400(
        self, client: AsyncClient, admin_token: str, hot_listings: list[str],
    ) -> None:
        dup_ids = [hot_listings[0], hot_listings[0]]
        response = await client.put(
            "/hot-listings/reorder",
            json={"listing_ids": dup_ids},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    async def test_agent_cannot_reorder_hot_listings(
        self, client: AsyncClient, agent_token: str, hot_listings: list[str],
    ) -> None:
        response = await client.put(
            "/hot-listings/reorder",
            json={"listing_ids": hot_listings},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403
