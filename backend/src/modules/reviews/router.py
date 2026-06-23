from fastapi import APIRouter, Depends, status

from src.modules.reviews.facades.create_review import create_review
from src.modules.reviews.facades.delete_review import delete_review
from src.modules.reviews.facades.get_review_detail import get_review_detail
from src.modules.reviews.facades.list_reviews import list_reviews
from src.modules.reviews.schemas import ReviewListResponse, ReviewResponse

router = APIRouter(prefix="/properties/{property_id}/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review_endpoint(result: ReviewResponse = Depends(create_review)):
    return result


@router.get("/", response_model=ReviewListResponse)
async def list_reviews_endpoint(result: ReviewListResponse = Depends(list_reviews)):
    return result


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review_endpoint(result: ReviewResponse = Depends(get_review_detail)):
    return result


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_endpoint(result: None = Depends(delete_review)):
    return result
