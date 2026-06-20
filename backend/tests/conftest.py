import subprocess
import time
import uuid
from collections.abc import AsyncGenerator

import bcrypt as _bcrypt

_original_gensalt = _bcrypt.gensalt
_bcrypt.gensalt = lambda rounds=4: _original_gensalt(rounds=rounds)  # noqa: E731

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.data.entities._base import Base
from src.data.entities.user import UserEntity, UserRole
from src.main import app
from src.platform.config import settings
from src.platform.dependencies import get_db
from src.platform.security import create_jwt

ADMIN_UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")
AGENT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000002")
DEACTIVATED_UUID = uuid.UUID("00000000-0000-0000-0000-000000000003")

_ADMIN_PWH = _bcrypt.hashpw(b"admin123", _bcrypt.gensalt(rounds=4)).decode()
_AGENT_PWH = _bcrypt.hashpw(b"agent123", _bcrypt.gensalt(rounds=4)).decode()
_DEACTIVATED_PWH = _bcrypt.hashpw(b"deac123", _bcrypt.gensalt(rounds=4)).decode()

TEST_PG_CONTAINER = "biglands-test-pg"

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(settings.test_database_url, echo=False, poolclass=NullPool)
    return _engine


@pytest.fixture(scope="session", autouse=True)
def docker_postgres():
    r = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Status}}", TEST_PG_CONTAINER],
        capture_output=True, text=True,
    )
    status = r.stdout.strip() if r.returncode == 0 else ""

    if status == "running":
        yield
        return
    elif status:
        subprocess.run(["docker", "start", TEST_PG_CONTAINER], capture_output=True)
    else:
        subprocess.run(
            [
                "docker", "run", "-d",
                "--name", TEST_PG_CONTAINER,
                "-e", "POSTGRES_USER=postgres",
                "-e", "POSTGRES_PASSWORD=postgres",
                "-e", "POSTGRES_DB=biglands_test",
                "-p", "5445:5432",
                "postgres:16-alpine",
            ],
            check=True, capture_output=True,
        )

    for _ in range(30):
        r = subprocess.run(
            ["docker", "exec", TEST_PG_CONTAINER, "pg_isready", "-U", "postgres"],
            capture_output=True,
        )
        if r.returncode == 0:
            break
        time.sleep(1)
    else:
        raise RuntimeError("Test PostgreSQL did not become ready in time")

    yield


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_schema(docker_postgres):
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def seed_users(setup_schema):
    admin = UserEntity(
        id=ADMIN_UUID,
        full_name="Admin User",
        username="admin",
        password_hash=_ADMIN_PWH,
        phone="0900000001",
        email="admin@biglands.com",
        role=UserRole.ADMIN,
        is_active=True,
    )
    agent = UserEntity(
        id=AGENT_UUID,
        full_name="Agent User",
        username="agent",
        password_hash=_AGENT_PWH,
        phone="0900000002",
        email="agent@biglands.com",
        role=UserRole.AGENT,
        is_active=True,
    )
    deactivated = UserEntity(
        id=DEACTIVATED_UUID,
        full_name="Deactivated User",
        username="deactivated",
        password_hash=_DEACTIVATED_PWH,
        phone="0900000003",
        email="deac@biglands.com",
        role=UserRole.AGENT,
        is_active=False,
    )
    async with AsyncSession(get_engine()) as session:
        session.add_all([admin, agent, deactivated])
        await session.commit()


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    conn = await get_engine().connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)
    yield session
    await session.close()
    await trans.rollback()
    await conn.close()


@pytest_asyncio.fixture
async def override_get_db(db_session: AsyncSession) -> AsyncGenerator[None, None]:
    async def _get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(override_get_db: None) -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def admin_token() -> str:
    return create_jwt(ADMIN_UUID, UserRole.ADMIN.value)


@pytest_asyncio.fixture
async def agent_token() -> str:
    return create_jwt(AGENT_UUID, UserRole.AGENT.value)
