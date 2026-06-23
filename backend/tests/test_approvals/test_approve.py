import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.usefixtures("seed_lookups")


@pytest.mark.asyncio
async def test_admin_can_approve_post_pending(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    prop_id, approval_id = post_pending_approval

    response = await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": "Approved"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    assert data["decision"]["reason"] == "Approved"

    prop_resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert prop_resp.json()["status"] == "available"


@pytest.mark.asyncio
async def test_approver_can_approve(
    client: AsyncClient, approver_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval

    response = await client.post(
        f"/approvals/{approval_id}/approve",
        json={},
        headers={"Authorization": f"Bearer {approver_token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "approved"


@pytest.mark.asyncio
async def test_sale_cannot_approve(
    client: AsyncClient, agent_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval

    response = await client.post(
        f"/approvals/{approval_id}/approve",
        json={},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cannot_approve_already_approved(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    await client.post(
        f"/approvals/{approval_id}/approve",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/approvals/{approval_id}/approve",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_approve_without_auth_fails(
    client: AsyncClient, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    response = await client.post(f"/approvals/{approval_id}/approve", json={})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_approve_nonexistent_returns_404(
    client: AsyncClient, admin_token: str,
) -> None:
    response = await client.post(
        f"/approvals/00000000-0000-0000-0000-000000009999/approve",
        json={},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
