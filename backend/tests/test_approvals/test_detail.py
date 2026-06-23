import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_approval_detail(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    assert approval_id is not None

    response = await client.get(
        f"/approvals/{approval_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(approval_id)
    assert data["status"] == "pending"
    assert data["transaction_type"] == "SELL"
    assert data["property"] is not None
    assert "request" in data
    assert data["request"]["action"] == "submit"
    assert data["request"]["to_status"] == "post_pending"
    assert data["decision"] is None
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_approval_detail_with_decision(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": "Looks good"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.get(
        f"/approvals/{approval_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    assert data["decision"] is not None
    assert data["decision"]["reason"] == "Looks good"
    assert "decided_by" in data["decision"]
    assert "decided_at" in data["decision"]


@pytest.mark.asyncio
async def test_get_nonexistent_approval_returns_404(
    client: AsyncClient, admin_token: str,
) -> None:
    response = await client.get(
        f"/approvals/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_approval_without_auth_fails(
    client: AsyncClient, post_pending_approval: tuple,
) -> None:
    _, approval_id = post_pending_approval
    response = await client.get(f"/approvals/{approval_id}")
    assert response.status_code == 401
