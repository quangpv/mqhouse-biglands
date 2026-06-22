from src.data.entities.listing import ListingEntity
from src.data.entities.user import UserEntity, UserRole
from src.modules.listings.schemas import CreatorInfo, ListingResponse


def listing_to_response(
    entity: ListingEntity,
    current_user: UserEntity | None = None,
) -> ListingResponse:
    creator = None
    if entity.created_by is not None:
        creator = CreatorInfo(
            id=entity.created_by.id,
            fullName=entity.created_by.full_name,
            phone=entity.created_by.phone,
        )
    price_per_m2 = entity.price / entity.total_area if entity.total_area > 0 else None

    can_view_phone = (
        current_user is None
        or current_user.role in (UserRole.ADMIN, UserRole.APPROVER)
        or (entity.created_by_id == current_user.id)
    )

    return ListingResponse(
        id=entity.id,
        code=entity.code,
        transaction_type=entity.transaction_type,
        property_type=entity.property_type,
        title=entity.title,
        description=entity.description,
        price=entity.price,
        commission_type=entity.commission_type,
        commission_value=entity.commission_value,
        area_width=entity.area_width,
        area_length=entity.area_length,
        total_area=entity.total_area,
        price_per_m2=price_per_m2,
        num_rooms=entity.num_rooms,
        num_bathrooms=entity.num_bathrooms,
        num_floors=entity.num_floors,
        street_name=entity.street_name,
        house_number=entity.house_number,
        address=entity.address,
        ward=entity.ward,
        district=entity.district,
        city=entity.city,
        latitude=entity.latitude,
        longitude=entity.longitude,
        label=entity.label,
        furnishing=entity.furnishing,
        frontage_type=entity.frontage_type,
        legal_status=entity.legal_status,
        direction=entity.direction,
        road_width=entity.road_width,
        owner_phone=entity.owner_phone if can_view_phone else None,
        video_url=entity.video_url,
        status=entity.status,
        is_hot=entity.is_hot,
        hot_order=entity.hot_order,
        view_count=entity.view_count,
        created_by_id=entity.created_by_id,
        creator=creator,
        approved_by_id=entity.approved_by_id,
        approved_at=entity.approved_at,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
