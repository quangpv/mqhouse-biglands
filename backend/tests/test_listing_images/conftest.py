import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity, ListingStatus, PropertyType, TransactionType, CommissionType
from src.data.entities.listing_image import ListingImageEntity
from src.shared.utils.code_generator import generate_product_code
from tests.conftest import AGENT_UUID, ADMIN_UUID


@dataclass
class ListingWithImages:
    listing_id: str
    image_ids: list[str]


def _make_listing(owner_id, status):
    return ListingEntity(
        id=uuid.uuid4(),
        code=generate_product_code(),
        transaction_type=TransactionType.BAN,
        property_type=PropertyType.CHDV,
        description=f"Image test {uuid.uuid4().hex[:8]}",
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


def _make_image(listing_id, url, order, is_primary):
    return ListingImageEntity(
        id=uuid.uuid4(),
        listing_id=listing_id,
        url=url,
        order=order,
        is_primary=is_primary,
    )


@pytest_asyncio.fixture
async def agent_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def admin_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(ADMIN_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def agent_listing_with_images(db_session: AsyncSession) -> ListingWithImages:
    listing = _make_listing(AGENT_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()

    ids = []
    for i in range(3):
        img = _make_image(listing.id, f"http://test.com/img_{i}.jpg", i + 1, i == 0)
        db_session.add(img)
        await db_session.flush()
        ids.append(str(img.id))

    return ListingWithImages(listing_id=str(listing.id), image_ids=ids)


@pytest_asyncio.fixture
async def admin_listing_with_images(db_session: AsyncSession) -> ListingWithImages:
    listing = _make_listing(ADMIN_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()

    ids = []
    for i in range(2):
        img = _make_image(listing.id, f"http://test.com/admin_img_{i}.jpg", i + 1, i == 0)
        db_session.add(img)
        await db_session.flush()
        ids.append(str(img.id))

    return ListingWithImages(listing_id=str(listing.id), image_ids=ids)
