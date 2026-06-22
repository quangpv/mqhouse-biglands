import uuid
from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.deal_event import DealEventEntity, DealEventType
from src.data.entities.listing import ListingEntity, ListingStatus, PropertyType, TransactionType, CommissionType
from src.shared.utils.code_generator import generate_product_code
from tests.conftest import ADMIN_UUID, AGENT_UUID, APPROVER_UUID


@pytest_asyncio.fixture
async def pending_admin_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(ADMIN_UUID, ListingStatus.PENDING_APPROVAL)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def pending_approver_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(APPROVER_UUID, ListingStatus.PENDING_APPROVAL)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def pending_approval_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.PENDING_APPROVAL)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def con_hang_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.CON_HANG)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def da_coc_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.DA_COC)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def draft_listing(db_session: AsyncSession) -> str:
    listing = _make_listing(AGENT_UUID, ListingStatus.DRAFT)
    db_session.add(listing)
    await db_session.flush()
    return str(listing.id)


@pytest_asyncio.fixture
async def pending_deposit_listing(db_session: AsyncSession, con_hang_listing: str) -> str:
    listing_id = uuid.UUID(con_hang_listing)
    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.DEPOSIT_REPORTED,
        reported_by_id=AGENT_UUID,
        customer_name="Nguyễn Văn A",
        deposit_amount=Decimal("100000000"),
    )
    db_session.add(event)
    await db_session.flush()
    return con_hang_listing


@pytest_asyncio.fixture
async def pending_closure_listing(db_session: AsyncSession, da_coc_listing: str) -> str:
    listing_id = uuid.UUID(da_coc_listing)
    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.CLOSURE_REPORTED,
        reported_by_id=AGENT_UUID,
    )
    db_session.add(event)
    await db_session.flush()
    return da_coc_listing


@pytest_asyncio.fixture
async def pending_cancellation_listing(db_session: AsyncSession, da_coc_listing: str) -> str:
    listing_id = uuid.UUID(da_coc_listing)
    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.CANCELLATION_REPORTED,
        reported_by_id=AGENT_UUID,
        notes="Khách thay đổi ý định",
    )
    db_session.add(event)
    await db_session.flush()
    return da_coc_listing


@pytest_asyncio.fixture
async def pending_sold_out_listing(db_session: AsyncSession, con_hang_listing: str) -> str:
    listing_id = uuid.UUID(con_hang_listing)
    event = DealEventEntity(
        listing_id=listing_id,
        event_type=DealEventType.SOLD_OUT_REPORTED,
        reported_by_id=AGENT_UUID,
    )
    db_session.add(event)
    await db_session.flush()
    return con_hang_listing


def _make_listing(owner_id, status):
    return ListingEntity(
        id=uuid.uuid4(),
        code=generate_product_code(),
        transaction_type=TransactionType.BAN,
        property_type=PropertyType.CHDV,
        description=f"Test listing for approvals {uuid.uuid4().hex[:8]}",
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
