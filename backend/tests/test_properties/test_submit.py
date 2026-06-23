import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_submit_property_by_sale(client: AsyncClient, agent_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": "Please approve"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "post_pending"
    assert data["requires_approval"] is True


@pytest.mark.asyncio
async def test_submit_property_by_admin(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "available"


@pytest.mark.asyncio
async def test_submit_property_wrong_status_fails(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_submit_property_not_owner_fails(client: AsyncClient, admin_token: str, agent_token: str,
                                                property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_submit_property_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/properties/00000000-0000-0000-0000-000000009999/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_submit_property_unauthorized(client: AsyncClient) -> None:
    response = await client.post(
        "/properties/00000000-0000-0000-0000-000000009999/transitions/submit",
        json={"notes": None},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_property_creates_notification_for_admins_and_approvers(
    client: AsyncClient, agent_token: str, property_payload: dict, db_session,
) -> None:
    from sqlalchemy import select
    from src.data.entities.notification import NotificationEntity
    from tests.conftest import ADMIN_UUID, APPROVER_UUID

    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": "Please approve"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200

    result = await db_session.execute(
        select(NotificationEntity).where(
            NotificationEntity.user_id.in_([ADMIN_UUID, APPROVER_UUID]),
            NotificationEntity.reference_id == prop_id,
        ),
    )
    notifications = result.scalars().all()
    assert len(notifications) == 2
    assert all(n.event_type == "listing_post_created" for n in notifications)
    assert all(n.is_read is False for n in notifications)
