from src.data.entities.pin import PinEntity
from src.modules.pins.schemas import PinResponse
from src.modules.properties.mapper import entity_to_response as property_to_response
from src.modules.properties.schemas import PropertyResponse


def entity_to_pin_response(entity: PinEntity) -> PinResponse:
    return PinResponse(message="Pinned")


def entity_to_property_response(entity: PinEntity) -> PropertyResponse:
    return property_to_response(entity.property)
