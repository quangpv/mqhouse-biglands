import uuid

from fastapi import Depends, HTTPException, status
from fastapi.responses import Response

from src.data.entities.listing import ListingStatus
from src.data.entities.user import UserEntity
from src.data.repositories.listing_repo import ListingRepo
from src.platform.auth import get_current_user
from src.shared.errors.exceptions import NotFoundError


async def delete_listing(
    listing_id: uuid.UUID,
    current_user: UserEntity = Depends(get_current_user),
    repo: ListingRepo = Depends(ListingRepo),
) -> Response:
    listing = await repo.get(listing_id)
    if listing is None:
        raise NotFoundError("Listing not found")

    if listing.created_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the listing owner can delete")

    if listing.status != ListingStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only DRAFT listings can be deleted. Withdraw the listing first.",
        )

    await repo.delete(listing_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
