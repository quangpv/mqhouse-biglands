import pytest
from httpx import AsyncClient

from tests.conftest import ADMIN_UUID


pytestmark = pytest.mark.usefixtures("seed_lookups")


@pytest.mark.asyncio
async def test_deposit_property_by_admin(client: AsyncClient, admin_token: str, property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={
            "customer_name": "John Buyer",
            "customer_phone": "0900000099",
            "contract_date": "2026-12-31",
            "notes": "Deposit received",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deposited"


@pytest.mark.asyncio
async def test_deposit_property_by_sale(client: AsyncClient, agent_token: str, admin_token: str,
                                        property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={
            "customer_name": "John Buyer",
            "customer_phone": "0900000099",
            "contract_date": "2026-12-31",
        },
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "deposit_pending"


@pytest.mark.asyncio
async def test_deposit_property_wrong_status_fails(client: AsyncClient, admin_token: str,
                                                    property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]

    response = await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={
            "customer_name": "John Buyer",
            "customer_phone": "0900000099",
            "contract_date": "2026-12-31",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_deposit_property_missing_customer_info_fails(client: AsyncClient, admin_token: str,
                                                            property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={"contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_deposit_property_past_contract_date_fails(client: AsyncClient, admin_token: str,
                                                         property_payload: dict) -> None:
    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={
            "customer_name": "John Buyer",
            "customer_phone": "0900000099",
            "contract_date": "2020-01-01",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_deposit_property_max_files(client: AsyncClient, admin_token: str, db_session,
                                          property_payload: dict) -> None:
    from src.data.entities.file import EntityType, FileEntity
    files = []
    for i in range(11):
        f = FileEntity(origin_name=f"test_{i}.jpg", path=f"/uploads/test_{i}.jpg",
                       mimetype="image/jpeg", size=1024, entity_type=EntityType.PROPERTY,
                       created_by_id=ADMIN_UUID)
        db_session.add(f)
        await db_session.flush()
        files.append(str(f.id))
    await db_session.commit()

    create_resp = await client.post(
        "/properties", json=property_payload, headers={"Authorization": f"Bearer {admin_token}"},
    )
    prop_id = create_resp.json()["id"]
    await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = await client.post(
        f"/properties/{prop_id}/transitions/deposit",
        json={
            "customer_name": "John Buyer",
            "customer_phone": "0900000099",
            "contract_date": "2026-12-31",
            "file_ids": files,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_deposit_property_not_found(client: AsyncClient, admin_token: str) -> None:
    response = await client.post(
        "/properties/00000000-0000-0000-0000-000000009999/transitions/deposit",
        json={"customer_name": "x", "customer_phone": "0900000000", "contract_date": "2026-12-31"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
