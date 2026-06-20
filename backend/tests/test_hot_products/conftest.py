import uuid
from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity, ListingStatus, PropertyType, TransactionType, CommissionType
from src.shared.utils.code_generator import generate_product_code
from tests.conftest import ADMIN_UUID


@pytest_asyncio.fixture
async def con_hang_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(ADMIN_UUID, ListingStatus.CON_HANG)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def draft_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(ADMIN_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def hot_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(ADMIN_UUID, ListingStatus.CON_HANG)
    listing.is_hot = True
    listing.hot_order = 1
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def hot_listings(db_session: AsyncSession) -> list[str]:
    ids = []
    for i in range(3):
        listing = _make_listing(ADMIN_UUID, ListingStatus.CON_HANG)
        listing.is_hot = True
        listing.hot_order = i + 1
        db_session.add(listing)
        ids.append(str(listing.id))
    await db_session.flush()
    return ids


def _make_listing(owner_id, status):
    return ListingEntity(
        id=uuid.uuid4(),
        code=generate_product_code(),
        transaction_type=TransactionType.BAN,
        property_type=PropertyType.CHDV,
        description=f"Test listing for hot products {uuid.uuid4().hex[:8]}",
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
