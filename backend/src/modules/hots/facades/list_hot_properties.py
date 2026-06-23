from fastapi import Depends

from src.data.repositories.hot_property_repo import HotPropertyRepo
from src.modules.hots.mapper import entity_to_response
from src.modules.hots.schemas import HotPropertyListResponse


async def list_hot_properties(
    repo: HotPropertyRepo = Depends(HotPropertyRepo),
) -> HotPropertyListResponse:
    rows = await repo.list_active()
    return [entity_to_response(r) for r in rows]
