import pytest
from httpx import AsyncClient

from tests.test_reviews.conftest import REVIEW_LISTING_ID

pytestmark = pytest.mark.asyncio


class TestCreateReview:
    async def test_authenticated_user_can_create_review(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json={"content": "Nice property!"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Nice property!"
        assert data["listing_id"] == str(REVIEW_LISTING_ID)

    async def test_cannot_create_duplicate_review_for_same_listing(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        payload = {"content": "Another review"}
        response1 = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json=payload,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response1.status_code == 201

        response2 = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json=payload,
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response2.status_code == 409

    async def test_create_review_with_empty_content_returns_400(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json={"content": ""},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 422

    async def test_unauthenticated_user_cannot_create_review(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(
            f"/listings/{REVIEW_LISTING_ID}/reviews",
            json={"content": "Should fail"},
        )
        assert response.status_code == 401
