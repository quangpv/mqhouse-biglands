import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.property_type import PropertyTypeEntity
from src.data.entities.transaction_type import TransactionTypeEntity


TX_TYPE_ID = uuid.UUID("00000000-0000-0000-0000-0000000000f1")
PT_TYPE_ID = uuid.UUID("00000000-0000-0000-0000-0000000000f2")


@pytest_asyncio.fixture
async def seed_lookups(db_session: AsyncSession):
    tx = TransactionTypeEntity(id=TX_TYPE_ID, code="SELL", display_name="Sell")
    pt = PropertyTypeEntity(id=PT_TYPE_ID, code="HOUSE", display_name="House")
    db_session.add_all([tx, pt])
    await db_session.commit()


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
