from src.data.entities.user import UserEntity, UserPropertyTypeEntity, UserTransactionTypeEntity
from src.modules.users.schemas import CreateUserRequest, UpdateUserRequest, UserResponse
from src.platform.security import hash_password


def request_to_entity(body: CreateUserRequest) -> UserEntity:
    entity = UserEntity(
        full_name=body.full_name,
        username=body.username,
        phone=body.phone,
        email=body.email,
        password_hash=hash_password(body.password),
        role=body.role,
        organization_id=body.organization_id,
    )
    entity.transaction_types = [
        UserTransactionTypeEntity(transaction_type_id=tid) for tid in body.transaction_type_ids
    ]
    entity.property_types = [
        UserPropertyTypeEntity(property_type_id=pid) for pid in body.property_type_ids
    ]
    return entity


def apply_to_entity(entity: UserEntity, body: UpdateUserRequest) -> UserEntity:
    if body.full_name is not None:
        entity.full_name = body.full_name
    if body.phone is not None:
        entity.phone = body.phone
    if body.email is not None:
        entity.email = body.email
    if body.is_active is not None:
        entity.is_active = body.is_active
    if body.organization_id is not None:
        entity.organization_id = body.organization_id
    if body.role is not None:
        entity.role = body.role
    if body.transaction_type_ids is not None:
        entity.transaction_types = [
            UserTransactionTypeEntity(transaction_type_id=tid) for tid in body.transaction_type_ids
        ]
    if body.property_type_ids is not None:
        entity.property_types = [
            UserPropertyTypeEntity(property_type_id=pid) for pid in body.property_type_ids
        ]
    return entity


def entity_to_response(entity: UserEntity) -> UserResponse:
    return UserResponse(
        id=entity.id,
        full_name=entity.full_name,
        username=entity.username,
        phone=entity.phone,
        email=entity.email,
        role=entity.role,
        is_active=entity.is_active,
        organization_id=str(entity.organization_id) if entity.organization_id else None,
        organization_name=entity.organization.display_name if entity.organization else None,
        property_type_ids=[pt.property_type_id for pt in entity.property_types],
        transaction_type_ids=[tt.transaction_type_id for tt in entity.transaction_types],
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
