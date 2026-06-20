import uuid

from fastapi import APIRouter, Depends, UploadFile, status

from src.modules.listing_images.facades.delete_image import delete_image
from src.modules.listing_images.facades.reorder_images import reorder_images
from src.modules.listing_images.facades.set_primary_image import set_primary_image
from src.modules.listing_images.facades.upload_image import upload_image
from src.modules.listing_images.schemas import ImageResponse, ReorderImagesRequest
from src.platform.auth import require_role

router = APIRouter(prefix="/listings/{listing_id}/images", tags=["listing_images"])


@router.post("", response_model=ImageResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "ADMIN"))])
async def upload(result: ImageResponse = Depends(upload_image)):
    return result


@router.put("/reorder", response_model=list[ImageResponse], dependencies=[Depends(require_role("AGENT", "ADMIN"))])
async def reorder(result: list[ImageResponse] = Depends(reorder_images)):
    return result


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("AGENT", "ADMIN"))])
async def delete(result = Depends(delete_image)):
    return result


@router.put("/{image_id}/primary", response_model=ImageResponse, dependencies=[Depends(require_role("AGENT", "ADMIN"))])
async def set_primary(result: ImageResponse = Depends(set_primary_image)):
    return result
