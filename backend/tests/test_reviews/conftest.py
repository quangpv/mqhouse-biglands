import uuid

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.listing import ListingEntity, ListingStatus, PropertyType, TransactionType, CommissionType
from src.data.entities.review import ReviewEntity
from src.data.entities.review_image import ReviewImageEntity
from src.data.entities.user import UserEntity, UserRole
from src.platform.security import hash_password
from tests.conftest import AGENT_UUID, get_engine

REVIEW_LISTING_ID = uuid.UUID("00000000-0000-0000-0000-000000000051")
REVIEW_AUTHOR_UUID = uuid.UUID("00000000-0000-0000-0000-000000000052")
REVIEW_ID = uuid.UUID("00000000-0000-0000-0000-000000000053")
REVIEW_IMAGE_ID = uuid.UUID("00000000-0000-0000-0000-000000000054")


def _make_listing(id, owner_id, status, code):
    return ListingEntity(
        id=id,
        code=code,
        transaction_type=TransactionType.BAN,
        property_type=PropertyType.CHDV,
        description=f"Review test listing {code}",
        price=5000000000,
        commission_type=CommissionType.PERCENTAGE,
        commission_value=1.5,
        area_width=5.0,
        area_length=20.0,
        total_area=100.0,
        num_rooms=2,
        num_bathrooms=1,
        num_floors=1,
        street_name="Test Street",
        house_number="1",
        address="1 Test Street",
        ward="Test Ward",
        district="Test District",
        city="Hồ Chí Minh",
        owner_phone="0900000001",
        created_by_id=owner_id,
        status=status,
    )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def seed_reviews(seed_organizations):
    async with AsyncSession(get_engine()) as session:
        review_author = UserEntity(
            id=REVIEW_AUTHOR_UUID,
            full_name="Review Author",
            username="reviewauthor",
            password_hash=hash_password("test123"),
            phone="0900000004",
            email="review@biglands.com",
            role=UserRole.AGENT,
            is_active=True,
        )
        session.add(review_author)
        await session.flush()

        listing = _make_listing(REVIEW_LISTING_ID, AGENT_UUID, ListingStatus.CON_HANG, "2501010000100")
        session.add(listing)
        await session.flush()

        review = ReviewEntity(
            id=REVIEW_ID,
            listing_id=REVIEW_LISTING_ID,
            author_id=REVIEW_AUTHOR_UUID,
            author_name="Review Author",
            content="Great listing!",
        )
        session.add(review)
        await session.flush()

        image = ReviewImageEntity(
            id=REVIEW_IMAGE_ID,
            review_id=REVIEW_ID,
            url="http://test.com/review-img.jpg",
            order=1,
        )
        session.add(image)
        await session.commit()
