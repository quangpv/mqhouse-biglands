import pytest
from httpx import AsyncClient

from tests.test_reviews.conftest import REVIEW_LISTING_ID

pytestmark = pytest.mark.asyncio


class TestDeleteReview:
    async def test_author_can_delete_own_review(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        create_resp = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json={"content": "To delete"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert create_resp.status_code == 201
        review_id = create_resp.json()["id"]

        response = await client.delete(
            f"/listings/{REVIEW_LISTING_ID}/reviews/{review_id}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 204

    async def test_admin_can_delete_any_review(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        create_resp = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json={"content": "Admin will delete this"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_resp.status_code == 201
        review_id = create_resp.json()["id"]

        response = await client.delete(
            f"/listings/{REVIEW_LISTING_ID}/reviews/{review_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

    async def test_non_author_non_admin_cannot_delete_review(
        self, client: AsyncClient, admin_token: str, agent_token: str,
    ) -> None:
        create_resp = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json={"content": "Admin owned review"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_resp.status_code == 201
        review_id = create_resp.json()["id"]

        response = await client.delete(
            f"/listings/{REVIEW_LISTING_ID}/reviews/{review_id}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_delete_nonexistent_review_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.delete(
            f"/listings/{REVIEW_LISTING_ID}/reviews/00000000-0000-0000-0000-000000009999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
