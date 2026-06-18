import pytest
from httpx import AsyncClient

from tests.test_listing_images.conftest import ListingWithImages

pytestmark = pytest.mark.asyncio


class TestDeleteImage:
    async def test_owner_can_delete_an_image_from_their_listing(
        self, client: AsyncClient, agent_token: str, agent_listing_with_images: ListingWithImages,
    ) -> None:
        image_id = agent_listing_with_images.image_ids[0]
        response = await client.delete(
            f"/listings/{agent_listing_with_images.listing_id}/images/{image_id}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 204

    async def test_non_owner_cannot_delete_an_image(
        self, client: AsyncClient, agent_token: str, admin_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.delete(
            f"/listings/{admin_listing_with_images.listing_id}/images/{admin_listing_with_images.image_ids[0]}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_deleting_a_non_existent_image_returns_not_found(
        self, client: AsyncClient, agent_token: str, agent_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.delete(
            f"/listings/{agent_listing_with_images.listing_id}/images/00000000-0000-0000-0000-000000000099",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_deleting_from_a_non_existent_listing_returns_not_found(
        self, client: AsyncClient, agent_token: str,
    ) -> None:
        response = await client.delete(
            "/listings/00000000-0000-0000-0000-000000000099/images/00000000-0000-0000-0000-000000000099",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_delete_images(
        self, client: AsyncClient, agent_listing_with_images: ListingWithImages,
    ) -> None:
        response = await client.delete(
            f"/listings/{agent_listing_with_images.listing_id}/images/{agent_listing_with_images.image_ids[0]}",
        )
        assert response.status_code == 401
