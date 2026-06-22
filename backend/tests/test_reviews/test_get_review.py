import pytest
from httpx import AsyncClient

from tests.test_reviews.conftest import REVIEW_ID, REVIEW_IMAGE_ID, REVIEW_LISTING_ID

pytestmark = pytest.mark.asyncio


class TestGetReview:
    async def test_can_get_review_by_id(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            f"/listings/{REVIEW_LISTING_ID}/reviews/{REVIEW_ID}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(REVIEW_ID)
        assert data["content"] == "Great listing!"
        assert data["author_name"] == "Review Author"
        assert len(data["images"]) >= 1

    async def test_get_nonexistent_review_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.get(
            f"/listings/{REVIEW_LISTING_ID}/reviews/00000000-0000-0000-0000-000000009999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
