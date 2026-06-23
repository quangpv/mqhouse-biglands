import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.user import UserEntity


@pytest.mark.asyncio
async def test_agent_with_valid_credentials_can_log_in(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_fails_when_username_does_not_exist(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "nonexistent", "password": "admin123"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_fails_when_password_is_incorrect(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "admin", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_deactivated_account_cannot_log_in(client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"username": "deactivated", "password": "deac123"},
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Account is deactivated"


@pytest.mark.asyncio
async def test_sale_device_limit_same_device_succeeds(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    result = await db_session.execute(
        select(UserEntity).where(UserEntity.username == "agent")
    )
    agent = result.scalar_one()
    agent.device_limit_enabled = True
    agent.device_id = None
    await db_session.commit()

    for _ in range(2):
        response = await client.post(
            "/auth/login",
            json={"username": "agent", "password": "agent123"},
            headers={"X-Device-Token": "device-A"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_sale_device_limit_denied_on_other_device_flow(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    result = await db_session.execute(
        select(UserEntity).where(UserEntity.username == "agent")
    )
    agent = result.scalar_one()
    agent.device_limit_enabled = True
    agent.device_id = None
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"username": "agent", "password": "agent123"},
        headers={"X-Device-Token": "device-A"},
    )
    assert response.status_code == 200

    response = await client.post(
        "/auth/login",
        json={"username": "agent", "password": "agent123"},
        headers={"X-Device-Token": "device-B"},
    )
    assert response.status_code == 403
    assert response.json()["message"] == "Device mismatch — login not allowed from this device"


@pytest.mark.asyncio
async def test_sale_device_limit_no_header_returns_403(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    result = await db_session.execute(
        select(UserEntity).where(UserEntity.username == "agent")
    )
    agent = result.scalar_one()
    agent.device_limit_enabled = True
    agent.device_id = None
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"username": "agent", "password": "agent123"},
    )
    assert response.status_code == 403
    assert response.json()["message"] == "X-Device-Token header is required"


@pytest.mark.asyncio
async def test_sale_device_limit_disabled_allows_any_device(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    result = await db_session.execute(
        select(UserEntity).where(UserEntity.username == "agent")
    )
    agent = result.scalar_one()
    agent.device_limit_enabled = False
    agent.device_id = None
    await db_session.commit()

    response_a = await client.post(
        "/auth/login",
        json={"username": "agent", "password": "agent123"},
        headers={"X-Device-Token": "device-A"},
    )
    assert response_a.status_code == 200

    response_b = await client.post(
        "/auth/login",
        json={"username": "agent", "password": "agent123"},
        headers={"X-Device-Token": "device-B"},
    )
    assert response_b.status_code == 200


@pytest.mark.asyncio
async def test_sale_device_limit_disabled_no_header_succeeds(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    result = await db_session.execute(
        select(UserEntity).where(UserEntity.username == "agent")
    )
    agent = result.scalar_one()
    agent.device_limit_enabled = False
    agent.device_id = None
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"username": "agent", "password": "agent123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_admin_device_limit_exempt(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    result = await db_session.execute(
        select(UserEntity).where(UserEntity.username == "admin")
    )
    admin = result.scalar_one()
    admin.device_limit_enabled = True
    admin.device_id = None
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
