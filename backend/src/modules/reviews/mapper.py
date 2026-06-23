import uuid

from src.data.entities.file import EntityType
from src.data.entities.review import ReviewEntity
from src.modules.reviews.schemas import CreateReviewRequest, FileInfo, ReviewResponse


def request_to_entity(
    body: CreateReviewRequest,
    property_id: uuid.UUID,
    author_id: uuid.UUID,
    author_name: str,
) -> ReviewEntity:
    return ReviewEntity(
        property_id=property_id,
        author_id=author_id,
        author_name=author_name,
        content=body.content,
    )


def entity_to_response(entity: ReviewEntity) -> ReviewResponse:
    images = []
    for rf in entity.images:
        f = rf.file
        if f is None:
            continue
        images.append(FileInfo(
            id=f.id,
            origin_name=f.origin_name,
            path=f.path,
            mimetype=f.mimetype,
            created_by=f.created_by_id,
            entity_type=f.entity_type.value if isinstance(f.entity_type, EntityType) else f.entity_type,
            size=f.size,
        ))

    return ReviewResponse(
        id=entity.id,
        property_id=entity.property_id,
        author_id=entity.author_id,
        author_name=entity.author_name,
        content=entity.content,
        images=images,
        created_at=entity.created_at,
        updated_at=entity.updated_at or entity.created_at,
    )
