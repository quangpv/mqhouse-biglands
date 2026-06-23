import uuid
from datetime import datetime, timezone

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.approval import ApprovalEntity, ApprovalStatus
from src.data.entities.property import CommissionType, PropertyEntity, PropertyStatus
from src.data.entities.property_transition import Action, PropertyTransitionEntity
from tests.conftest import AGENT_UUID, PT_TYPE_ID, TX_TYPE_ID


@pytest_asyncio.fixture
async def property_payload() -> dict:
    return {
        "type": "draft",
        "transaction_type_id": str(TX_TYPE_ID),
        "property_type_id": str(PT_TYPE_ID),
        "description": "Approval test property",
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
async def post_pending_approval(db_session: AsyncSession) -> tuple[uuid.UUID, uuid.UUID]:
    now = datetime.now(timezone.utc)
    prop_id = uuid.uuid4()
    transition_id = uuid.uuid4()
    approval_id = uuid.uuid4()

    prop = PropertyEntity(
        id=prop_id,
        code=f"POST-{uuid.uuid4().hex[:8].upper()}",
        transaction_type_id=TX_TYPE_ID,
        property_type_id=PT_TYPE_ID,
        description="Approval test property",
        price=5000000000,
        commission_type=CommissionType.PERCENTAGE,
        commission_value=2,
        area_width=5.0,
        area_length=20.0,
        total_area=100.0,
        num_rooms=3,
        num_bathrooms=2,
        num_floors=1,
        street_name="Main Street",
        house_number="123",
        address="123 Main Street, Ward 1",
        ward="Ward 1",
        district="District 1",
        city="Ho Chi Minh City",
        status=PropertyStatus.POST_PENDING,
        created_by_id=AGENT_UUID,
    )
    db_session.add(prop)

    transition = PropertyTransitionEntity(
        id=transition_id,
        property_id=prop_id,
        from_status=PropertyStatus.DRAFT,
        to_status=PropertyStatus.POST_PENDING,
        action=Action.SUBMIT,
        actor_id=AGENT_UUID,
        actor_name="Agent User",
        created_at=now,
    )
    db_session.add(transition)

    approval = ApprovalEntity(
        id=approval_id,
        property_id=prop_id,
        transition_id=transition_id,
        transaction_type_id=TX_TYPE_ID,
        status=ApprovalStatus.PENDING,
    )
    db_session.add(approval)
    await db_session.commit()

    return prop_id, approval_id


@pytest_asyncio.fixture
async def edit_pending_approval(db_session: AsyncSession) -> tuple[uuid.UUID, uuid.UUID]:
    now = datetime.now(timezone.utc)
    prop_id = uuid.uuid4()
    transition_id = uuid.uuid4()
    approval_id = uuid.uuid4()

    prop = PropertyEntity(
        id=prop_id,
        code=f"EDIT-{uuid.uuid4().hex[:8].upper()}",
        transaction_type_id=TX_TYPE_ID,
        property_type_id=PT_TYPE_ID,
        description="Approval test property",
        price=5000000000,
        commission_type=CommissionType.PERCENTAGE,
        commission_value=2,
        area_width=5.0,
        area_length=20.0,
        total_area=100.0,
        num_rooms=3,
        num_bathrooms=2,
        num_floors=1,
        street_name="Main Street",
        house_number="123",
        address="123 Main Street, Ward 1",
        ward="Ward 1",
        district="District 1",
        city="Ho Chi Minh City",
        status=PropertyStatus.EDIT_PENDING,
        created_by_id=AGENT_UUID,
    )
    db_session.add(prop)

    transition = PropertyTransitionEntity(
        id=transition_id,
        property_id=prop_id,
        from_status=PropertyStatus.AVAILABLE,
        to_status=PropertyStatus.EDIT_PENDING,
        action=Action.EDIT,
        actor_id=AGENT_UUID,
        actor_name="Agent User",
        created_at=now,
    )
    db_session.add(transition)

    approval = ApprovalEntity(
        id=approval_id,
        property_id=prop_id,
        transition_id=transition_id,
        transaction_type_id=TX_TYPE_ID,
        status=ApprovalStatus.PENDING,
        old_values={"price": 5000000000, "description": "Approval test property"},
    )
    db_session.add(approval)
    await db_session.commit()

    return prop_id, approval_id
