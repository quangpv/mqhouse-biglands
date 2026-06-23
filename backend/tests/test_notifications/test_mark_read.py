import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_mark_read_success(
    client: AsyncClient, admin_token: str, admin_notifications: list,
) -> None:
    nid = admin_notifications[0].id
    response = await client.patch(
        f"/notifications/{nid}/read",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(nid)
    assert data["is_read"] is True


@pytest.mark.asyncio
async def test_mark_read_not_owner(
    client: AsyncClient, agent_token: str, admin_notifications: list,
) -> None:
    nid = admin_notifications[0].id
    response = await client.patch(
        f"/notifications/{nid}/read",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_mark_read_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.patch(
        "/notifications/00000000-0000-0000-0000-000000009999/read",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
