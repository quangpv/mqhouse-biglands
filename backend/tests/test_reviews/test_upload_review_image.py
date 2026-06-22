import pytest
from httpx import AsyncClient

from tests.test_reviews.conftest import REVIEW_LISTING_ID

pytestmark = pytest.mark.asyncio


class TestUploadReviewImage:
    async def test_can_upload_image_to_review(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        create_resp = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json={"content": "Review with image"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_resp.status_code == 201
        review_id = create_resp.json()["id"]

        response = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews/{review_id}/images",
            files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"]
        assert data["url"].startswith("/uploads/")
        assert data["order"] == 1
