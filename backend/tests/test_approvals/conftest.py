import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient
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
async def post_pending_approval(
    client: AsyncClient, agent_token: str, admin_token: str, seed_lookups: None, property_payload: dict,
) -> tuple[uuid.UUID, uuid.UUID]:
    create_resp = await client.post(
        "/properties",
        json=property_payload,
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = uuid.UUID(create_resp.json()["id"])

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": "Please approve"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approvals = list_resp.json()["data"]
    approval_id = uuid.UUID(approvals[0]["id"]) if approvals else None

    return prop_id, approval_id


@pytest_asyncio.fixture
async def deposit_pending_approval(
    client: AsyncClient, agent_token: str, admin_token: str, seed_lookups: None, property_payload: dict,
) -> tuple[uuid.UUID, uuid.UUID]:
    create_resp = await client.post(
        "/properties",
        json=property_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = uuid.UUID(create_resp.json()["id"])

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={
            "customer_name": "John Buyer",
            "customer_phone": "0900000099",
            "contract_date": "2026-12-31",
        },
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approvals = list_resp.json()["data"]
    approval_id = uuid.UUID(approvals[0]["id"]) if approvals else None

    return prop_id, approval_id


@pytest_asyncio.fixture
async def soldout_pending_approval(
    client: AsyncClient, agent_token: str, admin_token: str, seed_lookups: None, property_payload: dict,
) -> tuple[uuid.UUID, uuid.UUID]:
    create_resp = await client.post(
        "/properties",
        json=property_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = uuid.UUID(create_resp.json()["id"])

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={
            "customer_name": "John Buyer",
            "customer_phone": "0900000099",
            "contract_date": "2026-12-31",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    await client.post(
        f"/properties/{prop_id}/transitions/soldout",
        json={"notes": "Sold out"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approvals = list_resp.json()["data"]
    approval_id = uuid.UUID(approvals[0]["id"]) if approvals else None

    return prop_id, approval_id


@pytest_asyncio.fixture
async def edit_pending_approval(
    client: AsyncClient, agent_token: str, admin_token: str, seed_lookups: None, property_payload: dict,
) -> tuple[uuid.UUID, uuid.UUID]:
    create_resp = await client.post(
        "/properties",
        json=property_payload,
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = uuid.UUID(create_resp.json()["id"])

    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    await client.put(
        f"/properties/{prop_id}",
        json={"price": 7000000000, "description": "Updated description"},
        headers={"Authorization": f"Bearer {agent_token}"},
    )

    list_resp = await client.get(
        "/approvals",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    approvals = list_resp.json()["data"]
    approval_id = uuid.UUID(approvals[0]["id"]) if approvals else None

    return prop_id, approval_id
