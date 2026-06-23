from fastapi import Depends, Query

from src.data.entities.user import UserEntity
from src.data.repositories._base import Repo
from src.data.repositories.pin_repo import PinRepo
from src.modules.pins.mapper import entity_to_property_response
from src.modules.properties.schemas import PageDTO
from src.modules.pins.schemas import MyPinListResponse
from src.platform.auth import get_current_user


async def list_my_pins(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    repo: PinRepo = Depends(PinRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> MyPinListResponse:
    rows, total = await repo.list_by_user(current_user.id, page=page, size=size)
    total_pages = Repo.calc_total_pages(total, size)
    return MyPinListResponse(
        data=[entity_to_property_response(r) for r in rows],
        metadata=PageDTO(page=page, size=size, total_pages=total_pages),
    )
