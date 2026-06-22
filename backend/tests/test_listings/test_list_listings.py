import pytest
from httpx import AsyncClient

from tests.conftest import ADMIN_UUID, AGENT_UUID
from tests.test_listings.conftest import CON_HANG_AGENT_ID, CON_HANG_AGENT_2_ID, CON_HANG_ADMIN_ID, PENDING_AGENT_ID

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

    async def test_listing_response_includes_filter_counts(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "filter_counts" in data
        assert "all" in data["filter_counts"]
        assert "hot" in data["filter_counts"]
        assert "pinned" in data["filter_counts"]
        assert data["filter_counts"]["all"] >= 3
        assert data["filter_counts"]["hot"] >= 0

    async def test_listing_response_includes_creator(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"createdBy": "me"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 1
        for item in data:
            assert "creator" in item
            assert "id" in item["creator"]
            assert "fullName" in item["creator"]
            assert "phone" in item["creator"]
            assert item["creator"]["fullName"] == "Admin User"

    async def test_listing_response_includes_price_per_m2(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 1
        for item in data:
            assert "price_per_m2" in item
            assert item["price_per_m2"] is not None

    async def test_listings_can_be_filtered_by_multiple_statuses(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"status": ["CON_HANG", "PENDING_APPROVAL"]},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        ids = {d["id"] for d in data}
        assert str(CON_HANG_ADMIN_ID) in ids
        assert str(CON_HANG_AGENT_ID) in ids
        assert str(PENDING_AGENT_ID) in ids
        statuses = {d["status"] for d in data}
        assert statuses == {"CON_HANG", "PENDING_APPROVAL"}

    async def test_listings_can_be_filtered_by_is_hot(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"isHot": "true"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        for item in data:
            assert item["is_hot"] is True

    async def test_created_by_me_filters_by_current_user(
        self, client: AsyncClient, admin_token: str, agent_token: str,
    ) -> None:
        response = await client.get(
            "/listings",
            params={"createdBy": "me"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        ids = {d["id"] for d in data}
        assert str(CON_HANG_ADMIN_ID) in ids
        assert str(CON_HANG_AGENT_ID) not in ids

    async def test_unauthenticated_user_cannot_list_listings(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get("/listings")
        assert response.status_code == 401
