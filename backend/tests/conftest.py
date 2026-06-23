import socket
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
from src.data.entities.refresh_token import RefreshTokenEntity
from src.data.entities.token_blacklist import TokenBlacklistEntity
from src.data.entities.user import UserEntity, UserRole
from src.data.repositories.refresh_token_repo import RefreshTokenRepo
from src.data.repositories.token_blacklist_repo import TokenBlacklistRepo
from src.main import create_app

app = create_app(api_prefix="")
from src.platform.config import settings
from src.platform.dependencies import get_db, get_email_service
from src.platform.email import EmailService
from src.platform.security import create_jwt

ADMIN_UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")
AGENT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000002")
DEACTIVATED_UUID = uuid.UUID("00000000-0000-0000-0000-000000000003")
APPROVER_UUID = uuid.UUID("00000000-0000-0000-0000-000000000004")
ORG_MQ_LAND_ID = uuid.UUID("00000000-0000-0000-0000-000000000041")
ORG_ID_LAND_ID = uuid.UUID("00000000-0000-0000-0000-000000000042")

_ADMIN_PWH = _bcrypt.hashpw(b"admin123", _bcrypt.gensalt(rounds=4)).decode()
_AGENT_PWH = _bcrypt.hashpw(b"agent123", _bcrypt.gensalt(rounds=4)).decode()
_DEACTIVATED_PWH = _bcrypt.hashpw(b"deac123", _bcrypt.gensalt(rounds=4)).decode()
_APPROVER_PWH = _bcrypt.hashpw(b"approver123", _bcrypt.gensalt(rounds=4)).decode()

TEST_PG_CONTAINER = "biglands-test-pg"

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(settings.test_database_url, echo=False, poolclass=NullPool)
    return _engine


@pytest.fixture(scope="session", autouse=True)
def docker_postgres():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        s.connect(("localhost", 5445))
        s.close()
        yield
        return
    except (ConnectionRefusedError, OSError):
        pass
    finally:
        s.close()

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
        role=UserRole.SALE,
        is_active=True,
    )
    approver = UserEntity(
        id=APPROVER_UUID,
        full_name="Approver User",
        username="approver",
        password_hash=_APPROVER_PWH,
        phone="0900000004",
        email="approver@biglands.com",
        role=UserRole.APPROVER,
        is_active=True,
    )
    deactivated = UserEntity(
        id=DEACTIVATED_UUID,
        full_name="Deactivated User",
        username="deactivated",
        password_hash=_DEACTIVATED_PWH,
        phone="0900000003",
        email="deac@biglands.com",
        role=UserRole.SALE,
        is_active=False,
    )
    async with AsyncSession(get_engine()) as session:
        session.add_all([admin, agent, approver, deactivated])
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
    return create_jwt(AGENT_UUID, UserRole.SALE.value)


@pytest_asyncio.fixture
async def approver_token() -> str:
    return create_jwt(APPROVER_UUID, UserRole.APPROVER.value)


class FakeEmailService(EmailService):
    def __init__(self):
        self.sent_emails: list[dict] = []

    async def send_password_reset(self, email: str, token: str) -> None:
        self.sent_emails.append({"email": email, "token": token})


@pytest_asyncio.fixture
async def fake_email_service() -> FakeEmailService:
    return FakeEmailService()


@pytest_asyncio.fixture
async def override_email_service(fake_email_service: FakeEmailService) -> None:
    app.dependency_overrides[get_email_service] = lambda: fake_email_service
    yield
    app.dependency_overrides.clear()
