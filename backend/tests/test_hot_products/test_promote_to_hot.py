import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestPromoteToHot:
    async def test_admin_promotes_a_con_hang_listing_to_hot(
        self, client: AsyncClient, admin_token: str, con_hang_listing: str,
    ) -> None:
        response = await client.post(
            "/api/v1/hot-listings",
            json={"listing_id": con_hang_listing},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["hot_order"] is not None
        assert data["hot_order"] == 1

    async def test_promoting_an_already_hot_listing_is_harmless(
        self, client: AsyncClient, admin_token: str, hot_listing: str,
    ) -> None:
        response = await client.post(
            "/api/v1/hot-listings",
            json={"listing_id": hot_listing},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["hot_order"] is not None

    async def test_admin_cannot_promote_a_draft_listing(
        self, client: AsyncClient, admin_token: str, draft_listing: str,
    ) -> None:
        response = await client.post(
            "/api/v1/hot-listings",
            json={"listing_id": draft_listing},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 409

    async def test_admin_cannot_promote_a_nonexistent_listing(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.post(
            "/api/v1/hot-listings",
            json={"listing_id": str(fake_id)},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_agent_cannot_promote_a_listing_to_hot(
        self, client: AsyncClient, agent_token: str, con_hang_listing: str,
    ) -> None:
        response = await client.post(
            "/api/v1/hot-listings",
            json={"listing_id": con_hang_listing},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_unauthenticated_user_cannot_promote(
        self, client: AsyncClient, con_hang_listing: str,
    ) -> None:
        response = await client.post(
            "/api/v1/hot-listings",
            json={"listing_id": con_hang_listing},
        )
        assert response.status_code == 401
