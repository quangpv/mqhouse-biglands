import uuid
from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity, ListingStatus, PropertyType, TransactionType, CommissionType
from src.data.entities.listing_image import ListingImageEntity
from src.shared.utils.code_generator import generate_product_code
from tests.conftest import AGENT_UUID, ADMIN_UUID, get_engine

# ── Session-scoped seed data (read-only) ──────────────────────
DRAFT_AGENT_ID = uuid.UUID("00000000-0000-0000-0000-000000000011")
CON_HANG_AGENT_ID = uuid.UUID("00000000-0000-0000-0000-000000000012")
PENDING_AGENT_ID = uuid.UUID("00000000-0000-0000-0000-000000000013")
CON_HANG_AGENT_2_ID = uuid.UUID("00000000-0000-0000-0000-000000000014")
DRAFT_ADMIN_ID = uuid.UUID("00000000-0000-0000-0000-000000000021")
CON_HANG_ADMIN_ID = uuid.UUID("00000000-0000-0000-0000-000000000022")
SEED_IMAGE_ID = uuid.UUID("00000000-0000-0000-0000-000000000031")


def _seed_listing(id, owner_id, status, code, title="", price=5000000000):
    return ListingEntity(
        id=id,
        code=code,
        transaction_type=TransactionType.BAN,
        property_type=PropertyType.CHDV,
        title=title,
        description=f"Description for {title or code}",
        price=price,
        commission_type=CommissionType.PERCENTAGE,
        commission_value=Decimal("1.5"),
        area_width=Decimal("5.5"),
        area_length=Decimal("20.0"),
        total_area=Decimal("110.0"),
        num_rooms=2,
        num_bathrooms=1,
        num_floors=1,
        street_name="Nguyễn Huệ",
        house_number="123",
        address=f"123 Nguyễn Huệ, {title or code}",
        ward="Bến Nghé",
        district="Quận 1",
        city="Hồ Chí Minh",
        owner_phone="0912345678",
        created_by_id=owner_id,
        status=status,
    )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def seed_listings(seed_users):  # noqa: F811
    listings = [
        _seed_listing(DRAFT_AGENT_ID, AGENT_UUID, ListingStatus.DRAFT, "2501010000001", "Đẹp như mơ"),
        _seed_listing(CON_HANG_AGENT_ID, AGENT_UUID, ListingStatus.CON_HANG, "2501010000002", "Căn hộ cao cấp", price=8000000000),
        _seed_listing(PENDING_AGENT_ID, AGENT_UUID, ListingStatus.PENDING_APPROVAL, "2501010000003", "Đang chờ duyệt"),
        _seed_listing(CON_HANG_AGENT_2_ID, AGENT_UUID, ListingStatus.CON_HANG, "2501010000004", "Trung tâm quận 1", price=12000000000),
        _seed_listing(DRAFT_ADMIN_ID, ADMIN_UUID, ListingStatus.DRAFT, "2501010000005", "Admin draft"),
        _seed_listing(CON_HANG_ADMIN_ID, ADMIN_UUID, ListingStatus.CON_HANG, "2501010000006", "Admin hot deal", price=6000000000),
    ]
    image = ListingImageEntity(
        id=SEED_IMAGE_ID,
        listing_id=DRAFT_AGENT_ID,
        url="http://test.com/image1.jpg",
        order=1,
        is_primary=True,
    )
    async with AsyncSession(get_engine()) as session:
        session.add_all(listings)
        session.add(image)
        await session.commit()


# ── Per-function fixtures (automatically rolled back) ────────

@pytest_asyncio.fixture
async def agent_draft(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def agent_con_hang(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.CON_HANG)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def agent_pending(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.PENDING_APPROVAL)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def admin_draft(db_session: AsyncSession) -> str:
    listing = _make_listing(ADMIN_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def admin_con_hang(db_session: AsyncSession) -> str:
    listing = _make_listing(ADMIN_UUID, ListingStatus.CON_HANG)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def agent_draft_with_image(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()
    image = ListingImageEntity(
        id=uuid.uuid4(),
        listing_id=listing.id,
        url="http://test.com/img.jpg",
        order=1,
        is_primary=True,
    )
    db_session.add(image)
    await db_session.flush()
    return str(listing.id)


def _make_listing(owner_id, status):
    return ListingEntity(
        id=uuid.uuid4(),
        code=generate_product_code(),
        transaction_type=TransactionType.BAN,
        property_type=PropertyType.CHDV,
        description=f"Test listing generated at {uuid.uuid4().hex[:8]}",
        price=Decimal("5000000000"),
        commission_type=CommissionType.PERCENTAGE,
        commission_value=Decimal("1.5"),
        area_width=Decimal("5.0"),
        area_length=Decimal("20.0"),
        total_area=Decimal("100.0"),
        street_name="Lê Lợi",
        house_number="45",
        address="45 Lê Lợi, Bến Nghé, Quận 1",
        ward="Bến Nghé",
        district="Quận 1",
        city="Hồ Chí Minh",
        owner_phone="0900000001",
        created_by_id=owner_id,
        status=status,
    )
