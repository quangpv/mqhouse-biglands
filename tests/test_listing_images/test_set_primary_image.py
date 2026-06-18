import pytest
from httpx import AsyncClient

from tests.test_listing_images.conftest import ListingWithImages

pytestmark = pytest.mark.asyncio


class TestSetPrimaryImage:
    async def test_owner_can_set_a_non_primary_image_as_cover(
        self, client: AsyncClient, agent_token: str, agent_listing_with_images: ListingWithImages,
    ) -> None:
        new_primary = agent_listing_with_images.image_ids[2]
        response = await client.put(
            f"/listings/{agent_listing_with_images.listing_id}/images/{new_primary}/primary",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_primary"] is True
        assert data["id"] == new_primary

    async def test_non_owner_cannot_set_primary_image(
        self, client: AsyncClient, agent_token: str, admin_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.put(
            f"/listings/{admin_listing_with_images.listing_id}/images/{admin_listing_with_images.image_ids[0]}/primary",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_setting_a_non_existent_image_as_primary_returns_not_found(
        self, client: AsyncClient, agent_token: str, agent_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.put(
            f"/listings/{agent_listing_with_images.listing_id}/images/00000000-0000-0000-0000-000000000099/primary",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_setting_primary_on_a_non_existent_listing_returns_not_found(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.put(
            "/listings/00000000-0000-0000-0000-000000000099/images/00000000-0000-0000-0000-000000000099/primary",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_set_primary_image(
        self, client: AsyncClient, agent_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.put(
            f"/listings/{agent_listing_with_images.listing_id}/images/{agent_listing_with_images.image_ids[0]}/primary",
        )
        assert response.status_code == 401
