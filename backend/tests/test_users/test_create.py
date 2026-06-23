import pytest
from httpx import AsyncClient

from tests.conftest import FakeEmailService


@pytest.mark.asyncio
async def test_admin_can_create_user(
    client: AsyncClient, admin_token: str,
    override_email_service: None, fake_email_service: FakeEmailService,
) -> None:
    response = await client.post(
        "/users/",
        json={
            "full_name": "New User",
            "username": "newuser",
            "phone": "0900000100",
            "email": "newuser@biglands.com",
            "password": "Pass123!",
            "role": "SALE",
            "organization_id": None,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "New User"
    assert data["username"] == "newuser"
    assert data["role"] == "SALE"
    assert data["is_active"] is True
    assert data["property_type_ids"] == []
    assert data["transaction_type_ids"] == []
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

    assert len(fake_email_service.sent_emails) == 1
    sent = fake_email_service.sent_emails[0]
    assert sent["email"] == "newuser@biglands.com"
    assert sent["username"] == "newuser"
    assert sent["password"] == "Pass123!"


@pytest.mark.asyncio
async def test_admin_can_create_user_with_type_ids(client: AsyncClient, admin_token: str) -> None:
    tx_resp = await client.post(
        "/transaction-types/",
        json={"code": "USER_TX", "display_name": "User Tx"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    tx_id = tx_resp.json()["id"]

    pt_resp = await client.post(
        "/property-types/",
        json={"code": "USER_PT", "display_name": "User Pt"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    pt_id = pt_resp.json()["id"]

    response = await client.post(
        "/users/",
        json={
            "full_name": "User With Types",
            "username": "userwithtypes",
            "password": "Pass123!",
            "role": "SALE",
            "property_type_ids": [pt_id],
            "transaction_type_ids": [tx_id],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["property_type_ids"] == [pt_id]
    assert data["transaction_type_ids"] == [tx_id]


@pytest.mark.asyncio
async def test_non_admin_cannot_create_user(client: AsyncClient, agent_token: str) -> None:
    response = await client.post(
        "/users/",
        json={
            "full_name": "Should Fail",
            "username": "shouldfail",
            "password": "Pass123!",
            "role": "SALE",
        },
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_user_without_auth_fails(client: AsyncClient) -> None:
    response = await client.post(
        "/users/",
        json={
            "full_name": "No Auth",
            "username": "noauth",
            "password": "Pass123!",
            "role": "SALE",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_user_duplicate_username_returns_409(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/users/",
        json={
            "full_name": "Duplicate Username",
            "username": "admin",
            "password": "Pass123!",
            "role": "SALE",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_duplicate_email_returns_409(client: AsyncClient, admin_token: str) -> None:
    await client.post(
        "/users/",
        json={
            "full_name": "First User",
            "username": "firstuser",
            "phone": "0900000101",
            "email": "dup@biglands.com",
            "password": "Pass123!",
            "role": "SALE",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await client.post(
        "/users/",
        json={
            "full_name": "Second User",
            "username": "seconduser",
            "phone": "0900000102",
            "email": "dup@biglands.com",
            "password": "Pass123!",
            "role": "SALE",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 409
