import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_all_success(
    client: AsyncClient, admin_token: str, admin_notifications: list,
) -> None:
    response = await client.post(
        "/notifications/read-all",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "All notifications marked as read"}

    unread_resp = await client.get(
        "/notifications/unread-count", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert unread_resp.json() == {"count": 0}


@pytest.mark.asyncio
async def test_read_all_no_notifications(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/notifications/read-all",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "All notifications marked as read"}
