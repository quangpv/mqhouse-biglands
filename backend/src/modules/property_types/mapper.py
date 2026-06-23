from src.data.entities.property_type import PropertyTypeEntity
from src.modules.property_types.schemas import PropertyTypeInfo, PropertyTypeResponse


def request_to_entity(body: PropertyTypeInfo) -> PropertyTypeEntity:
    return PropertyTypeEntity(code=body.code, display_name=body.display_name)


def apply_to_entity(entity: PropertyTypeEntity, body: PropertyTypeInfo) -> PropertyTypeEntity:
    entity.code = body.code
    entity.display_name = body.display_name
    return entity


def entity_to_response(entity: PropertyTypeEntity) -> PropertyTypeResponse:
    return PropertyTypeResponse(
        id=entity.id,
        code=entity.code,
        display_name=entity.display_name,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
