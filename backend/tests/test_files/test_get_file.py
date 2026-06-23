import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_get_file_metadata(client: AsyncClient, admin_token: str) -> None:
    upload_resp = await client.post(
        "/files/",
        files=[("files", ("test.jpg", b"test image content", "image/jpeg"))],
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    file_id = upload_resp.json()["file_ids"][0]

    response = await client.get(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(file_id)
    assert data["origin_name"] == "test.jpg"
    assert data["mimetype"] == "image/jpeg"
    assert data["size"] == 18
    assert data["created_by"] is not None


@pytest.mark.asyncio
async def test_get_nonexistent_file_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        f"/files/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
    assert response.json()["message"] == "File not found"


@pytest.mark.asyncio
async def test_get_file_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get(f"/files/{uuid.uuid4()}")
    assert response.status_code == 401
