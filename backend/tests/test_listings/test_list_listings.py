import pytest
from httpx import AsyncClient

from tests.test_listings.conftest import CON_HANG_AGENT_ID, CON_HANG_AGENT_2_ID, CON_HANG_ADMIN_ID

pytestmark = pytest.mark.asyncio


class TestListListings:
    async def test_admin_can_view_all_active_listings(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) >= 3
        assert data["total_count"] >= 3

    async def test_agent_can_only_view_their_own_listings(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        ids = {d["id"] for d in data}
        assert {str(CON_HANG_AGENT_ID), str(CON_HANG_AGENT_2_ID)} <= ids
        assert str(CON_HANG_ADMIN_ID) not in ids

    async def test_listings_can_be_paginated(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"page": 1, "size": 1},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        assert data["page"] == 1
        assert data["size"] == 1
        assert data["total"] >= 3

    async def test_listings_can_be_searched_by_title(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"search": "cao cấp"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 1

    async def test_listings_can_be_filtered_by_transaction_type(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"transaction_type": "BAN"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert all(l["transaction_type"] == "BAN" for l in data)

    async def test_listings_can_be_sorted_by_price_ascending(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"sort_by": "price", "sort_order": "asc"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        if len(data) >= 2:
            prices = [float(l["price"]) for l in data]
            assert prices == sorted(prices)

    async def test_unauthenticated_user_cannot_list_listings(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/listings")
        assert response.status_code == 401
