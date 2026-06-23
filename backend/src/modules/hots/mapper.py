from src.data.entities.hot_property import HotPropertyEntity
from src.modules.hots.schemas import HotPropertyResponse
from src.modules.properties.mapper import entity_to_response as property_to_response


def entity_to_response(entity: HotPropertyEntity) -> HotPropertyResponse:
    return HotPropertyResponse(
        id=entity.id,
        property=property_to_response(entity.property),
        start_time=entity.start_time,
        end_time=entity.end_time,
        created_by=entity.created_by_id,
        created_at=entity.created_at,
    )
