import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authenticated_user_can_upload_files(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/files/",
        files=[
            ("files", ("test.jpg", b"test image content", "image/jpeg")),
            ("files", ("test2.png", b"test png content", "image/png")),
        ],
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "file_ids" in data
    assert len(data["file_ids"]) == 2


@pytest.mark.asyncio
async def test_upload_with_no_files_fails(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/files/",
        files=[],
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_exceeding_max_file_count_fails(client: AsyncClient, admin_token: str) -> None:
    files = [("files", (f"file{i}.jpg", b"x", "image/jpeg")) for i in range(11)]
    response = await client.post(
        "/files/",
        files=files,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 400
    assert "Maximum 10 files allowed" in response.json()["message"]


@pytest.mark.asyncio
async def test_upload_exceeding_size_limit_fails(client: AsyncClient, admin_token: str) -> None:
    large_content = b"x" * (11 * 1024 * 1024)
    response = await client.post(
        "/files/",
        files=[("files", ("large.jpg", large_content, "image/jpeg"))],
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 400
    assert "exceeds 10MB" in response.json()["message"]


@pytest.mark.asyncio
async def test_upload_without_auth_fails(client: AsyncClient) -> None:
    response = await client.post(
        "/files/",
        files=[("files", ("test.jpg", b"content", "image/jpeg"))],
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_with_entity_type_optional(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/files/",
        data={"entity_type": "avatar"},
        files=[("files", ("avatar.png", b"avatar content", "image/png"))],
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["file_ids"]) == 1
