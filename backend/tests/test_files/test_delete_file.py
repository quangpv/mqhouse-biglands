import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_owner_can_delete_own_file(client: AsyncClient, agent_token: str) -> None:
    upload_resp = await client.post(
        "/files/",
        files=[("files", ("test.jpg", b"content", "image/jpeg"))],
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    file_id = upload_resp.json()["file_ids"][0]

    response = await client.delete(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_admin_can_delete_any_file(client: AsyncClient, agent_token: str, admin_token: str) -> None:
    upload_resp = await client.post(
        "/files/",
        files=[("files", ("test.jpg", b"content", "image/jpeg"))],
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    file_id = upload_resp.json()["file_ids"][0]

    response = await client.delete(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_non_owner_cannot_delete_file(client: AsyncClient, agent_token: str, approver_token: str) -> None:
    upload_resp = await client.post(
        "/files/",
        files=[("files", ("test.jpg", b"content", "image/jpeg"))],
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    file_id = upload_resp.json()["file_ids"][0]

    response = await client.delete(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {approver_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_nonexistent_file_returns_404(client: AsyncClient, admin_token: str) -> None:
    response = await client.delete(
        f"/files/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_file_without_auth_fails(client: AsyncClient) -> None:
    response = await client.delete(f"/files/{uuid.uuid4()}")
    assert response.status_code == 401
