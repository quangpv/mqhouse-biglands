import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_list_approvals(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    response = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 1
    assert "metadata" in data
    assert data["metadata"]["page"] == 1


@pytest.mark.asyncio
async def test_approver_can_list_approvals(
    client: AsyncClient, approver_token: str, post_pending_approval: tuple,
) -> None:
    response = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {approver_token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_sale_cannot_list_approvals(client: AsyncClient, agent_token: str) -> None:
    response = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_without_auth_fails(client: AsyncClient) -> None:
    response = await client.get("/approvals")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_pagination(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    response = await client.get(
        "/approvals?page=1&size=1",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) <= 1
    assert data["metadata"]["page"] == 1
    assert data["metadata"]["size"] == 1


@pytest.mark.asyncio
async def test_filter_by_status(
    client: AsyncClient, admin_token: str, post_pending_approval: tuple,
) -> None:
    response = await client.get(
        "/approvals?status=pending",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    for item in data["data"]:
        assert item["status"] == "pending"
