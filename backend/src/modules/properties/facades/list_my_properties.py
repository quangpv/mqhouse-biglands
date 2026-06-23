import uuid

from fastapi import Depends, Query

from src.data.entities.property import DirectionType, PropertyStatus
from src.data.entities.user import UserEntity
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import entity_to_response
from src.modules.properties.schemas import PageDTO, PropertyListResponse
from src.platform.auth import get_current_user


async def list_my_properties(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    transaction_type_id: list[uuid.UUID] = Query([]),
    property_type_id: list[uuid.UUID] = Query([]),
    district: list[str] = Query([]),
    ward: list[str] = Query([]),
    direction: list[DirectionType] = Query([]),
    room_count_from: int | None = Query(None),
    room_count_to: int | None = Query(None),
    area_from: float | None = Query(None),
    area_to: float | None = Query(None),
    width_from: float | None = Query(None),
    width_to: float | None = Query(None),
    price_from: float | None = Query(None),
    price_to: float | None = Query(None),
    status: list[str] = Query([]),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PropertyListResponse:
    from decimal import Decimal

    statuses: list[PropertyStatus] | None = None
    if status:
        statuses = [PropertyStatus(s) for s in status]

    tt_ids = transaction_type_id if transaction_type_id else None
    pt_ids = property_type_id if property_type_id else None
    districts = district if district else None
    wards_list = ward if ward else None
    directions = direction if direction else None

    rows, total = await repo.search(
        page=page,
        size=size,
        search=search,
        transaction_type_ids=tt_ids,
        property_type_ids=pt_ids,
        districts=districts,
        wards=wards_list,
        directions=directions,
        room_count_from=room_count_from,
        room_count_to=room_count_to,
        area_from=Decimal(str(area_from)) if area_from is not None else None,
        area_to=Decimal(str(area_to)) if area_to is not None else None,
        width_from=Decimal(str(width_from)) if width_from is not None else None,
        width_to=Decimal(str(width_to)) if width_to is not None else None,
        price_from=Decimal(str(price_from)) if price_from is not None else None,
        price_to=Decimal(str(price_to)) if price_to is not None else None,
        statuses=statuses,
        is_hot=None,
        created_by_id=current_user.id,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    total_pages = (total + size - 1) // size if total > 0 else 0

    return PropertyListResponse(
        data=[entity_to_response(row) for row in rows],
        metadata=PageDTO(page=page, size=size, total_pages=total_pages),
    )
