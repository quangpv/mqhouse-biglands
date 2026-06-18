import uuid

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.notification import NotificationEntity, ReferenceType
from tests.conftest import ADMIN_UUID, AGENT_UUID


@pytest_asyncio.fixture
async def agent_notification(db_session: AsyncSession) -> str:
    notif = NotificationEntity(
        id=uuid.uuid4(),
        user_id=AGENT_UUID,
        title="Your listing has been approved",
        body="Listing BĐS-001 has been approved and is now live.",
        reference_type=ReferenceType.LISTING,
        reference_id=uuid.uuid4(),
        is_read=False,
    )
    db_session.add(notif)
    await db_session.flush()
    return str(notif.id)


@pytest_asyncio.fixture
async def agent_notifications(db_session: AsyncSession) -> dict:
    notif1 = NotificationEntity(
        id=uuid.uuid4(),
        user_id=AGENT_UUID,
        title="Your listing has been approved",
        body="Listing BĐS-001 has been approved.",
        reference_type=ReferenceType.LISTING,
        reference_id=uuid.uuid4(),
        is_read=False,
    )
    notif2 = NotificationEntity(
        id=uuid.uuid4(),
        user_id=AGENT_UUID,
        title="Deposit reported on your listing",
        body="A deposit has been reported on BĐS-002.",
        reference_type=ReferenceType.DEAL_EVENT,
        reference_id=uuid.uuid4(),
        is_read=False,
    )
    notif3 = NotificationEntity(
        id=uuid.uuid4(),
        user_id=AGENT_UUID,
        title="Deal has been closed",
        body="The deal on BĐS-003 has been closed.",
        reference_type=ReferenceType.DEAL_EVENT,
        reference_id=uuid.uuid4(),
        is_read=True,
    )
    db_session.add_all([notif1, notif2, notif3])
    await db_session.flush()
    return {
        "unread_ids": [str(notif1.id), str(notif2.id)],
        "read_ids": [str(notif3.id)],
        "all_ids": [str(notif1.id), str(notif2.id), str(notif3.id)],
    }


@pytest_asyncio.fixture
async def admin_notification(db_session: AsyncSession) -> str:
    notif = NotificationEntity(
        id=uuid.uuid4(),
        user_id=ADMIN_UUID,
        title="New deposit report",
        body="A new deposit has been reported on listing BĐS-001.",
        reference_type=ReferenceType.DEAL_EVENT,
        reference_id=uuid.uuid4(),
        is_read=False,
    )
    db_session.add(notif)
    await db_session.flush()
    return str(notif.id)
