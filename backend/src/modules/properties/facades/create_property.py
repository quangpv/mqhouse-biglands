import logging
import random
from datetime import datetime

from fastapi import Depends

from src.data.entities.user import UserEntity
from src.data.repositories.property_repo import PropertyRepo
from src.modules.properties.mapper import entity_to_response, request_to_entity
from src.modules.properties.schemas import CreatePropertyRequest, PropertyResponse
from src.platform.auth import get_current_user

logger = logging.getLogger(__name__)


def _generate_code() -> str:
    date_part = datetime.now().strftime("%y%m%d")
    rand_part = f"{random.randint(0, 9999999):07d}"
    return f"{date_part}{rand_part}"


async def create_property(
    body: CreatePropertyRequest,
    repo: PropertyRepo = Depends(PropertyRepo),
    current_user: UserEntity = Depends(get_current_user),
) -> PropertyResponse:
    code = _generate_code()
    entity = request_to_entity(body, code=code, created_by_id=current_user.id)

    entity = await repo.save(entity)

    if body.image_ids:
        for i, fid in enumerate(body.image_ids):
            await repo.create_image(entity.id, fid, order=i, is_primary=(i == 0))

    reloaded = await repo.get(entity.id)
    assert reloaded is not None
    await repo.load_images(reloaded)
    result = entity_to_response(reloaded)
    return result
