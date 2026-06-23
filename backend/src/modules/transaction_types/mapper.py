from src.data.entities.transaction_type import TransactionTypeEntity
from src.modules.transaction_types.schemas import TransactionTypeResponse


def entity_to_response(entity: TransactionTypeEntity) -> TransactionTypeResponse:
    return TransactionTypeResponse(
        id=entity.id,
        code=entity.code,
        display_name=entity.display_name,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
