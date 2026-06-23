import uuid

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.notification import NotificationEntity
from tests.conftest import ADMIN_UUID, AGENT_UUID, PT_TYPE_ID, TX_TYPE_ID


@pytest_asyncio.fixture
async def property_payload() -> dict:
    return {
        "type": "draft",
        "transaction_type_id": str(TX_TYPE_ID),
        "property_type_id": str(PT_TYPE_ID),
        "description": "A nice property",
        "price": 5000000000,
        "commission_type": "PERCENTAGE",
        "commission_value": 2,
        "area_width": 5.0,
        "area_length": 20.0,
        "total_area": 100.0,
        "num_rooms": 3,
        "num_bathrooms": 2,
        "num_floors": 1,
        "street_name": "Main Street",
        "house_number": "123",
        "address": "123 Main Street, Ward 1",
        "ward": "Ward 1",
        "district": "District 1",
        "city": "Ho Chi Minh City",
    }


@pytest_asyncio.fixture
async def admin_notifications(db_session: AsyncSession) -> list[NotificationEntity]:
    from src.data.repositories.notification_repo import NotificationRepo

    repo = NotificationRepo(db=db_session)
    created = []
    for i in range(3):
        e = NotificationEntity(
            user_id=ADMIN_UUID,
            title=f"Notification {i + 1}",
            body=f"Body {i + 1}",
            reference_type="property",
            reference_id=uuid.uuid4(),
            is_read=i == 0,
            event_type="listing_post_created",
            actor_name="Agent User",
            transaction_type="BAN",
        )
        created.append(await repo.save(e))
    return created
