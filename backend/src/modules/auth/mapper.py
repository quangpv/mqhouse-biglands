from src.data.entities.user import UserEntity
from src.modules.auth.schemas import UserResponse


def user_to_response(entity: UserEntity) -> UserResponse:
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
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
