from src.data.entities.listing import ListingStatus
from src.shared.errors.exceptions import ConflictError


STATUS_TRANSITIONS: dict[ListingStatus, set[ListingStatus]] = {
    ListingStatus.DRAFT: {ListingStatus.PENDING_APPROVAL},
    ListingStatus.PENDING_APPROVAL: {ListingStatus.CON_HANG, ListingStatus.DRAFT},
    ListingStatus.CON_HANG: {ListingStatus.DA_COC, ListingStatus.HET_HANG, ListingStatus.DRAFT, ListingStatus.QUA_HAN},
    ListingStatus.DA_COC: {ListingStatus.DA_CHOT, ListingStatus.HUY_COC},
    ListingStatus.DA_CHOT: set(),
    ListingStatus.HUY_COC: set(),
    ListingStatus.HET_HANG: set(),
    ListingStatus.QUA_HAN: set(),
}


def validate_transition(from_status: ListingStatus, to_status: ListingStatus) -> None:
    allowed = STATUS_TRANSITIONS.get(from_status, set())
    if to_status not in allowed:
        msg = f"Cannot transition from {from_status.value} to {to_status.value}"
        raise ConflictError(detail=msg)
