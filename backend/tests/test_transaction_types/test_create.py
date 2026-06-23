import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_can_create_transaction_type(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/transaction-types/",
        json={"code": "BAN", "display_name": "Bán"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "BAN"
    assert data["display_name"] == "Bán"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_non_admin_cannot_create_transaction_type(client: AsyncClient, agent_token: str) -> None:
    response = await client.post(
        "/transaction-types/",
        json={"code": "CHO_THUE", "display_name": "Cho thuê"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_without_auth_fails(client: AsyncClient) -> None:
    response = await client.post(
        "/transaction-types/",
        json={"code": "SANG_NHUONG", "display_name": "Sang nhượng"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_duplicate_code_returns_409(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/transaction-types/",
        json={"code": "DUPLICATE", "display_name": "Original"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.post(
        "/transaction-types/",
        json={"code": "DUPLICATE", "display_name": "Duplicate"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
