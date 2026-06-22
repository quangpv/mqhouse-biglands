
from fastapi import APIRouter, Depends, status

from src.modules.listings.facades.create_listing import create_listing
from src.modules.listings.facades.list_listings import list_listings
from src.modules.listings.facades.get_listing import get_listing
from src.modules.listings.facades.update_listing import update_listing
from src.modules.listings.facades.delete_listing import delete_listing
from src.modules.listings.facades.submit_listing import submit_listing
from src.modules.listings.facades.withdraw_listing import withdraw_listing
from src.modules.listings.facades.get_filter_counts import get_filter_counts
from src.modules.listings.schemas import FilterCounts, ListingDetailResponse, ListingListResponse, ListingResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def create(result: ListingResponse = Depends(create_listing)):
    return result


@router.get("", response_model=ListingListResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def list_all(result: ListingListResponse = Depends(list_listings)):
    return result


@router.get("/filter-counts", response_model=FilterCounts, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def get_counts(result: FilterCounts = Depends(get_filter_counts)):
    return result


@router.get("/{listing_id}", response_model=ListingDetailResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def get(result: ListingDetailResponse = Depends(get_listing)):
    return result


@router.put("/{listing_id}", response_model=ListingResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def update(result: ListingResponse = Depends(update_listing)):
    return result


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def delete(result = Depends(delete_listing)):
    return result


@router.post("/{listing_id}/submit", response_model=ListingResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def submit(result: ListingResponse = Depends(submit_listing)):
    return result


@router.post("/{listing_id}/withdraw", response_model=ListingResponse, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def withdraw(result: ListingResponse = Depends(withdraw_listing)):
    return result
