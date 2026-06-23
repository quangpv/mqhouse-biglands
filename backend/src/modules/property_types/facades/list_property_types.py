from fastapi import Depends

from src.data.repositories.property_type_repo import PropertyTypeRepo
from src.modules.property_types.mapper import entity_to_response
from src.modules.property_types.schemas import PropertyTypeListResponse


async def list_property_types(
    repo: PropertyTypeRepo = Depends(PropertyTypeRepo),
) -> PropertyTypeListResponse:
    entities = await repo.get_all()
    return [entity_to_response(e) for e in entities]
