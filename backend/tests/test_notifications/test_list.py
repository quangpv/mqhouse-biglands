import pytest
from httpx import AsyncClient

from src.data.entities.notification import NotificationEntity


@pytest.mark.asyncio
async def test_list_notifications_empty(client: AsyncClient, admin_token: str) -> None:
    response = await client.get(
        "/notifications", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["metadata"]["total_pages"] == 0


@pytest.mark.asyncio
async def test_list_notifications_with_items(
    client: AsyncClient, admin_token: str, admin_notifications: list,
) -> None:
    response = await client.get(
        "/notifications", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 3
    assert data["metadata"]["page"] == 1
    assert data["metadata"]["size"] == 20
    assert data["metadata"]["total_pages"] == 1


@pytest.mark.asyncio
async def test_list_notifications_filter_unread(
    client: AsyncClient, admin_token: str, admin_notifications: list,
) -> None:
    response = await client.get(
        "/notifications?is_read=false", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert all(n["is_read"] is False for n in data["data"])


@pytest.mark.asyncio
async def test_list_notifications_filter_read(
    client: AsyncClient, admin_token: str, admin_notifications: list,
) -> None:
    response = await client.get(
        "/notifications?is_read=true", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["is_read"] is True


@pytest.mark.asyncio
async def test_list_notifications_pagination(
    client: AsyncClient, admin_token: str, db_session,
) -> None:
    from src.data.repositories.notification_repo import NotificationRepo
    from tests.conftest import ADMIN_UUID

    repo = NotificationRepo(db=db_session)
    for i in range(5):
        e = NotificationEntity(
            user_id=ADMIN_UUID, title=f"N{i}", body=None,
            reference_type=None, reference_id=None,
            is_read=False, event_type=None, actor_name=None, transaction_type=None,
        )
        await repo.save(e)

    response = await client.get(
        "/notifications?page=1&size=2", headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["metadata"]["page"] == 1
    assert data["metadata"]["size"] == 2
    assert data["metadata"]["total_pages"] == 3


@pytest.mark.asyncio
async def test_list_notifications_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/notifications")
    assert response.status_code == 401
