import pytest
from httpx import AsyncClient

from src.platform.config import settings

pytestmark = pytest.mark.asyncio


class TestUploadImage:
    async def test_owner_can_upload_a_jpeg_image_to_their_listing(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{agent_listing}/images",
            files={"file": ("photo.jpg", b"fake_jpeg_data", "image/jpeg")},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["listing_id"] == agent_listing
        assert data["order"] == 1
        assert data["is_primary"] is True
        assert data["url"].startswith("/uploads/")
        assert data["url"].endswith(".jpg")

    async def test_second_image_upload_is_not_marked_primary(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        await client.post(
            f"/listings/{agent_listing}/images",
            files={"file": ("first.jpg", b"data", "image/jpeg")},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        response = await client.post(
            f"/listings/{agent_listing}/images",
            files={"file": ("second.png", b"data", "image/png")},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["order"] == 2
        assert data["is_primary"] is False

    async def test_non_image_file_type_is_rejected(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{agent_listing}/images",
            files={"file": ("doc.pdf", b"%PDF-1.4 fake", "application/pdf")},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 400

    async def test_uploading_to_a_listing_at_the_20_image_limit_is_rejected(
        self, client: AsyncClient, agent_token: str, agent_listing: str,
    ) -> None:
        for _ in range(20):
            await client.post(
                f"/listings/{agent_listing}/images",
                files={"file": ("img.jpg", b"d", "image/jpeg")},
                headers={"Authorization": f"Bearer {agent_token}"},
            )
        response = await client.post(
            f"/listings/{agent_listing}/images",
            files={"file": ("extra.jpg", b"d", "image/jpeg")},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 409

    async def test_non_owner_cannot_upload_to_listing(
        self, client: AsyncClient, agent_token: str, admin_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{admin_listing}/images",
            files={"file": ("photo.jpg", b"data", "image/jpeg")},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert response.status_code == 403

    async def test_uploading_to_nonexistent_listing_returns_404(
        self, client: AsyncClient, admin_token: str,
    ) -> None:
        response = await client.post(
            "/listings/00000000-0000-0000-0000-000000000099/images",
            files={"file": ("photo.jpg", b"data", "image/jpeg")},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    async def test_unauthenticated_user_cannot_upload_images(
        self, client: AsyncClient, agent_listing: str,
    ) -> None:
        response = await client.post(
            f"/listings/{agent_listing}/images",
            files={"file": ("photo.jpg", b"data", "image/jpeg")},
        )
        assert response.status_code == 401
