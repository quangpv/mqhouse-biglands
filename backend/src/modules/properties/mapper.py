import uuid
from decimal import Decimal

from src.data.entities.property import PropertyEntity, PropertyStatus
from src.data.entities.property_image import PropertyImageEntity
from src.modules.properties.schemas import (
    CreatePropertyRequest,
    CreatorInfo,
    FileInfo,
    PropertyResponse,
    PropertyTransitionResponse,
    UpdatePropertyRequest,
)


def request_to_entity(body: CreatePropertyRequest, code: str, created_by_id: uuid.UUID) -> PropertyEntity:
    entity = PropertyEntity(
        code=code,
        transaction_type_id=body.transaction_type_id,
        property_type_id=body.property_type_id,
        title=body.title,
        description=body.description,
        price=body.price,
        commission_type=body.commission_type,
        commission_value=body.commission_value,
        area_width=body.area_width,
        area_length=body.area_length,
        total_area=body.total_area,
        num_rooms=body.num_rooms,
        num_bathrooms=body.num_bathrooms,
        num_floors=body.num_floors,
        street_name=body.street_name,
        house_number=body.house_number,
        address=body.address,
        ward=body.ward,
        district=body.district,
        city=body.city,
        latitude=body.latitude,
        longitude=body.longitude,
        label=body.label,
        furnishing=body.furnishing,
        frontage_type=body.frontage_type,
        legal_status=body.legal_status,
        direction=body.direction,
        road_width=body.road_width,
        owner_phone=body.owner_phone,
        video_url=body.video_url,
        status=PropertyStatus(body.type),
        created_by_id=created_by_id,
    )
    return entity


def apply_to_entity(entity: PropertyEntity, body: UpdatePropertyRequest) -> PropertyEntity:
    if body.transaction_type_id is not None:
        entity.transaction_type_id = body.transaction_type_id
    if body.property_type_id is not None:
        entity.property_type_id = body.property_type_id
    if body.title is not None:
        entity.title = body.title
    if body.description is not None:
        entity.description = body.description
    if body.price is not None:
        entity.price = body.price
    if body.commission_type is not None:
        entity.commission_type = body.commission_type
    if body.commission_value is not None:
        entity.commission_value = body.commission_value
    if body.area_width is not None:
        entity.area_width = body.area_width
    if body.area_length is not None:
        entity.area_length = body.area_length
    if body.total_area is not None:
        entity.total_area = body.total_area
    if body.num_rooms is not None:
        entity.num_rooms = body.num_rooms
    if body.num_bathrooms is not None:
        entity.num_bathrooms = body.num_bathrooms
    if body.num_floors is not None:
        entity.num_floors = body.num_floors
    if body.street_name is not None:
        entity.street_name = body.street_name
    if body.house_number is not None:
        entity.house_number = body.house_number
    if body.address is not None:
        entity.address = body.address
    if body.ward is not None:
        entity.ward = body.ward
    if body.district is not None:
        entity.district = body.district
    if body.city is not None:
        entity.city = body.city
    if body.latitude is not None:
        entity.latitude = body.latitude
    if body.longitude is not None:
        entity.longitude = body.longitude
    if body.label is not None:
        entity.label = body.label
    if body.furnishing is not None:
        entity.furnishing = body.furnishing
    if body.frontage_type is not None:
        entity.frontage_type = body.frontage_type
    if body.legal_status is not None:
        entity.legal_status = body.legal_status
    if body.direction is not None:
        entity.direction = body.direction
    if body.road_width is not None:
        entity.road_width = body.road_width
    if body.owner_phone is not None:
        entity.owner_phone = body.owner_phone
    if body.video_url is not None:
        entity.video_url = body.video_url
    return entity


def _compute_price_per_m2(entity: PropertyEntity) -> Decimal | None:
    if entity.price and entity.total_area and entity.total_area > 0:
        return Decimal(str(entity.price / entity.total_area)).quantize(Decimal("0.01"))
    return None


def _get_primary_image_url(images: list[PropertyImageEntity]) -> str | None:
    if not images:
        return None
    primary = next((img for img in images if img.is_primary), images[0])
    if primary.file and primary.file.path:
        return primary.file.path
    return None


def _build_file_info(image: PropertyImageEntity) -> FileInfo | None:
    f = image.file
    if f is None:
        return None
    return FileInfo(
        id=f.id,
        origin_name=f.origin_name,
        path=f.path,
        mimetype=f.mimetype,
        created_by=f.created_by_id,
        entity_type=f.entity_type.value if f.entity_type else "",
        size=f.size,
    )


def _requires_approval(status: PropertyStatus) -> bool:
    return status in (
        PropertyStatus.POST_PENDING,
        PropertyStatus.DEPOSIT_PENDING,
        PropertyStatus.SOLDOUT_PENDING,
        PropertyStatus.COMPLETE_PENDING,
        PropertyStatus.CANCEL_PENDING,
        PropertyStatus.EDIT_PENDING,
    )


def entity_to_response(
    entity: PropertyEntity,
    transaction_type_code: str | None = None,
    property_type_code: str | None = None,
    is_pinned: bool = False,
) -> PropertyResponse:
    creator_info: CreatorInfo | None = None
    if entity.creator:
        creator_info = CreatorInfo(
            id=entity.creator.id,
            full_name=entity.creator.full_name,
            phone=entity.creator.phone,
        )

    images = entity.images or []
    image_files: list[FileInfo] = []
    for img in images:
        fi = _build_file_info(img)
        if fi is not None:
            image_files.append(fi)

    if entity.transaction_type:
        transaction_type_code = entity.transaction_type.code
    if entity.property_type:
        property_type_code = entity.property_type.code

    return PropertyResponse(
        id=entity.id,
        code=entity.code,
        transaction_type_id=entity.transaction_type_id,
        transaction_type_code=transaction_type_code,
        property_type_id=entity.property_type_id,
        property_type_code=property_type_code,
        title=entity.title,
        description=entity.description,
        price=entity.price,
        commission_type=entity.commission_type,
        commission_value=entity.commission_value,
        area_width=entity.area_width,
        area_length=entity.area_length,
        total_area=entity.total_area,
        price_per_m2=_compute_price_per_m2(entity),
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
        owner_phone=entity.owner_phone,
        video_url=entity.video_url,
        status=entity.status,
        is_hot=entity.is_hot,
        hot_order=entity.hot_order,
        view_count=entity.view_count,
        primary_image_url=_get_primary_image_url(images),
        images=image_files,
        created_by_id=entity.created_by_id,
        creator=creator_info,
        is_pinned=is_pinned,
        requires_approval=_requires_approval(entity.status),
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def transition_to_response(transition) -> PropertyTransitionResponse:
    file_ids = [tf.file_id for tf in (transition.files or [])]
    return PropertyTransitionResponse(
        id=transition.id,
        property_id=transition.property_id,
        from_status=transition.from_status,
        to_status=transition.to_status,
        action=transition.action.value if transition.action else "",
        actor_id=transition.actor_id,
        actor_name=transition.actor_name,
        notes=transition.notes,
        customer_name=transition.customer_name,
        customer_phone=transition.customer_phone,
        contract_date=transition.contract_date,
        file_ids=file_ids,
        created_at=transition.created_at,
    )
