import uuid

from fastapi import Depends, Path

from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import transition_to_response
from src.modules.properties.schemas import PropertyTransitionListResponse
from src.shared.errors.exceptions import NotFoundError


async def get_status_logs(
    property_id: uuid.UUID = Path(..., alias="property_id"),
    repo: PropertyRepo = Depends(PropertyRepo),
) -> PropertyTransitionListResponse:
    entity = await repo.get(property_id)
    if not entity:
        raise NotFoundError("Property not found")

    transitions = await repo.get_transitions(property_id)
    return [transition_to_response(t) for t in transitions]
