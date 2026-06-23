import uuid

import pytest_asyncio
from httpx import AsyncClient

from tests.conftest import PT_TYPE_ID, TX_TYPE_ID

FILE_ID = uuid.UUID("00000000-0000-0000-0000-0000000000a1")


@pytest_asyncio.fixture
async def property_payload() -> dict:
    return {
        "type": "draft",
        "transaction_type_id": str(TX_TYPE_ID),
        "property_type_id": str(PT_TYPE_ID),
        "description": "Review test property",
        "price": 5000000000,
        "commission_type": "PERCENTAGE",
        "commission_value": 2,
        "area_width": 5.0,
        "area_length": 20.0,
        "total_area": 100.0,
        "num_rooms": 3,
        "num_bathrooms": 2,
        "num_floors": 1,
        "street_name": "Main St",
        "house_number": "1",
        "address": "1 Main St",
        "ward": "Ward 1",
        "district": "District 1",
        "city": "HCMC",
    }


@pytest_asyncio.fixture
async def reviewed_property(
    client: AsyncClient,
    agent_token: str,
    admin_token: str,
    property_payload: dict,
) -> uuid.UUID:
    resp = await client.post(
        "/properties",
        json=property_payload,
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    prop_id = uuid.UUID(resp.json()["id"])

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
    approval_id = approvals[0]["id"]

    await client.post(
        f"/approvals/{approval_id}/approve",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    resp = await client.get(
        f"/properties/{prop_id}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    return prop_id
