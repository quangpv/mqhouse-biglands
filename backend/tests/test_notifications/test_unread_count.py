import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_unread_count_zero(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/notifications/unread-count", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"count": 0}


@pytest.mark.asyncio
async def test_unread_count_after_creating(
    client: AsyncClient, admin_token: str, admin_notifications: list,
) -> None:
    response = await client.get(
        "/notifications/unread-count", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"count": 2}


@pytest.mark.asyncio
async def test_unread_count_other_user(
    client: AsyncClient, agent_token: str, admin_notifications: list,
) -> None:
    response = await client.get(
        "/notifications/unread-count", headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"count": 0}
