import pytest
from httpx import AsyncClient

from tests.test_listing_images.conftest import ListingWithImages

pytestmark = pytest.mark.asyncio


class TestReorderImages:
    async def test_owner_can_reorder_images_for_their_listing(
        self, client: AsyncClient, agent_token: str, agent_listing_with_images: ListingWithImages,
    ) -> None:
        ids = agent_listing_with_images.image_ids
        new_order = [ids[2], ids[1], ids[0]]
        response = await client.put(
            f"/listings/{agent_listing_with_images.listing_id}/images/reorder",
            json={"image_ids": new_order},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["id"] == ids[2]
        assert data[0]["order"] == 1
        assert data[0]["is_primary"] is True
        assert data[1]["id"] == ids[1]
        assert data[1]["order"] == 2
        assert data[1]["is_primary"] is False
        assert data[2]["id"] == ids[0]
        assert data[2]["order"] == 3
        assert data[2]["is_primary"] is False

    async def test_reorder_with_a_non_existent_image_id_returns_400(
        self, client: AsyncClient, agent_token: str, agent_listing_with_images: ListingWithImages,
    ) -> None:
        ids = agent_listing_with_images.image_ids
        response = await client.put(
            f"/listings/{agent_listing_with_images.listing_id}/images/reorder",
            json={"image_ids": [ids[0], "00000000-0000-0000-0000-000000000099"]},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 400

    async def test_non_owner_cannot_reorder_images(
        self, client: AsyncClient, agent_token: str, admin_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.put(
            f"/listings/{admin_listing_with_images.listing_id}/images/reorder",
            json={"image_ids": admin_listing_with_images.image_ids},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_reordering_images_on_a_non_existent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.put(
            "/listings/00000000-0000-0000-0000-000000000099/images/reorder",
            json={"image_ids": []},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_reorder_images(
        self, client: AsyncClient, agent_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.put(
            f"/listings/{agent_listing_with_images.listing_id}/images/reorder",
            json={"image_ids": agent_listing_with_images.image_ids},
        )
        assert response.status_code == 401
