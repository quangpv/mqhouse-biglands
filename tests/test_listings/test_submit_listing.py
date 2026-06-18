import uuid

import pytest
from httpx import AsyncClient

from tests.test_listings.conftest import CON_HANG_AGENT_ID, CON_HANG_ADMIN_ID

pytestmark = pytest.mark.asyncio


class TestSubmitListing:
    async def test_owner_can_submit_draft_listing_with_images(
        self, client: AsyncClient, agent_token: str, agent_draft_with_image: str,
    ) -> None:
        response = await client.post(
            f"/listings/{agent_draft_with_image}/submit",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "PENDING_APPROVAL"

    async def test_submit_draft_listing_without_image_returns_400(
        self, client: AsyncClient, agent_token: str, agent_draft: str,
    ) -> None:
        response = await client.post(
            f"/listings/{agent_draft}/submit",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 400

    async def test_non_owner_cannot_submit_listing(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            f"/listings/{CON_HANG_ADMIN_ID}/submit",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_submit_CON_HANG_listing_returns_409(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.post(
            f"/listings/{CON_HANG_AGENT_ID}/submit",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409

    async def test_submit_nonexistent_listing_returns_404(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            f"/listings/{fake_id}/submit",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_submit_listing(
        self, client: AsyncClient,
    ) -> None:
        response = await client.post(f"/listings/{CON_HANG_AGENT_ID}/submit")
        assert response.status_code == 401
