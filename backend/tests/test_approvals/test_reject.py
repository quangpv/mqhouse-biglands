import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_reject_post_pending(
    client: AsyncClient, admin_token: str, agent_token: str, post_pending_approval: tuple,
) -> None:
    prop_id, approval_id = post_pending_approval

    response = await client.post(
        f"/approvals/{approval_id}/reject",
        json={"reason": "Invalid info"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"
    assert data["decision"]["reason"] == "Invalid info"
    assert data["property"]["status"] == "draft"

    get_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert get_resp.json()["status"] == "draft"


@pytest.mark.asyncio
async def test_approver_can_reject(
    client: AsyncClient, approver_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval

    response = await client.post(
        f"/approvals/{approval_id}/reject",
        json={},
        headers={"Authorization": f"Bearer {approver_token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


@pytest.mark.asyncio
async def test_sale_cannot_reject(
    client: AsyncClient, agent_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval

    response = await client.post(
        f"/approvals/{approval_id}/reject",
        json={},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cannot_reject_already_rejected(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    await client.post(
        f"/approvals/{approval_id}/reject",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/approvals/{approval_id}/reject",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_reject_without_auth_fails(
    client: AsyncClient, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    response = await client.post(f"/approvals/{approval_id}/reject", json={})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_reject_nonexistent_returns_404(
    client: AsyncClient, admin_token: str,
) -> None:
    response = await client.post(
        "/approvals/00000000-0000-0000-0000-000000009999/reject",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_reject_creates_notification_for_property_owner(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple, db_session,
) -> None:
    from sqlalchemy import select
    from src.data.entities.notification import NotificationEntity
    from tests.conftest import AGENT_UUID

    _, approval_id = post_pending_approval

    response = await client.post(
        f"/approvals/{approval_id}/reject",
        json={"reason": "Invalid"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200

    result = await db_session.execute(
        select(NotificationEntity).where(NotificationEntity.user_id == AGENT_UUID),
    )
    notifications = result.scalars().all()
    assert len(notifications) >= 1
    assert notifications[0].event_type == "listing_post_rejected"
