from src.data.entities.file import FileEntity
from src.modules.files.schemas import FileInfoResponse


def file_entity_to_response(entity: FileEntity) -> FileInfoResponse:
    return FileInfoResponse(
        id=entity.id,
        origin_name=entity.origin_name,
        path=entity.path,
        mimetype=entity.mimetype,
        created_by=entity.created_by_id,
        entity_type=entity.entity_type,
        size=entity.size,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
