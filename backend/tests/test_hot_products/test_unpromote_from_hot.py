import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestUnpromoteFromHot:
    async def test_admin_removes_hot_status_and_badge_disappears(
        self, client: AsyncClient, admin_token: str, hot_listing: str,
    ) -> None:
        response = await client.delete(
            f"/api/v1/hot-listings/{hot_listing}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["hot_order"] is None

    async def test_admin_can_unpromote_a_non_hot_listing_without_error(
        self, client: AsyncClient, admin_token: str, con_hang_listing: str,
    ) -> None:
        response = await client.delete(
            f"/api/v1/hot-listings/{con_hang_listing}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200

    async def test_admin_cannot_unpromote_a_nonexistent_listing(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        fake_id = uuid.uuid4()
        response = await client.delete(
            f"/api/v1/hot-listings/{fake_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_agent_cannot_unpromote(
        self, client: AsyncClient, agent_token: str, hot_listing: str,
    ) -> None:
        response = await client.delete(
            f"/api/v1/hot-listings/{hot_listing}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_unauthenticated_user_cannot_unpromote(
        self, client: AsyncClient, hot_listing: str,
    ) -> None:
        response = await client.delete(f"/api/v1/hot-listings/{hot_listing}")
        assert response.status_code == 401
