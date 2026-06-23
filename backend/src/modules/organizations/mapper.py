from src.data.entities.organization import (
    OrganizationEntity,
    OrgPropertyTypeEntity,
    OrgTransactionTypeEntity,
)
from src.modules.organizations.schemas import OrganizationInfo, OrganizationResponse


def request_to_entity(body: OrganizationInfo) -> OrganizationEntity:
    entity = OrganizationEntity(name=body.name, display_name=body.display_name)
    entity.transaction_types = [
        OrgTransactionTypeEntity(transaction_type_id=tid) for tid in body.transaction_types
    ]
    entity.property_types = [
        OrgPropertyTypeEntity(property_type_id=pid) for pid in body.property_types
    ]
    return entity


def apply_to_entity(entity: OrganizationEntity, body: OrganizationInfo) -> OrganizationEntity:
    entity.name = body.name
    entity.display_name = body.display_name
    entity.transaction_types = [
        OrgTransactionTypeEntity(transaction_type_id=tid) for tid in body.transaction_types
    ]
    entity.property_types = [
        OrgPropertyTypeEntity(property_type_id=pid) for pid in body.property_types
    ]
    return entity


def entity_to_response(entity: OrganizationEntity) -> OrganizationResponse:
    return OrganizationResponse(
        id=entity.id,
        name=entity.name,
        display_name=entity.display_name,
        transaction_types=[a.transaction_type_id for a in entity.transaction_types],
        property_types=[a.property_type_id for a in entity.property_types],
        created_at=entity.created_at,
    )
