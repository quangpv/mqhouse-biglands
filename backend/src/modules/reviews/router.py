from fastapi import APIRouter, Depends, status

from src.modules.reviews.facades.create_review import create_review
from src.modules.reviews.facades.get_review import delete_review, get_review
from src.modules.reviews.facades.list_reviews import list_reviews
from src.modules.reviews.facades.upload_review_image import upload_review_image
from src.modules.reviews.schemas import ReviewImageResponse, ReviewListResponse, ReviewResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/listings/{listing_id}/reviews", tags=["reviews"])


@router.get("", response_model=ReviewListResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def list_all(result: ReviewListResponse = Depends(list_reviews)):
    return result


@router.get("/{review_id}", response_model=ReviewResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def get(result: ReviewResponse = Depends(get_review)):
    return result


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def create(result: ReviewResponse = Depends(create_review)):
    return result


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def delete(result = Depends(delete_review)):
    return result


@router.post("/{review_id}/images", response_model=ReviewImageResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def upload_image(result: ReviewImageResponse = Depends(upload_review_image)):
    return result
