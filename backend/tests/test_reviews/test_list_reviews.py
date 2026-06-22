import pytest
from httpx import AsyncClient

from tests.test_reviews.conftest import REVIEW_LISTING_ID

pytestmark = pytest.mark.asyncio


class TestListReviews:
    async def test_can_list_reviews_for_a_listing(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            f"/listings/{REVIEW_LISTING_ID}/reviews?page=1&size=20",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) >= 1
        assert data["data"][0]["content"] == "Great listing!"

    async def test_list_reviews_returns_paginated_response(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        body = response.json()
        assert "page" in body
        assert "size" in body
        assert "total" in body

    async def test_list_reviews_for_nonexistent_listing_returns_empty_list(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.get(
            "/listings/00000000-0000-0000-0000-000000009999/reviews",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["data"] == []

    async def test_unauthenticated_user_can_list_reviews(
        self, client: AsyncClient,
    ) -> None:
        response = await client.get(f"/listings/{REVIEW_LISTING_ID}/reviews")
        assert response.status_code == 401
