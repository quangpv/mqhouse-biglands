import uuid

from fastapi import APIRouter, Depends, status

from src.modules.deal_events.facades.report_cancellation import report_cancellation
from src.modules.deal_events.facades.report_closure import report_closure
from src.modules.deal_events.facades.report_deposit import report_deposit
from src.modules.deal_events.facades.report_sold_out import report_sold_out
from src.modules.deal_events.schemas import DealEventResponse
from src.platform.auth import require_role

router = APIRouter(prefix="/listings/{listing_id}/deal-events", tags=["deal_events"])


@router.post("/deposit", response_model=DealEventResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def deposit(result: DealEventResponse = Depends(report_deposit)):
    return result


@router.post("/closure", response_model=DealEventResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def closure(result: DealEventResponse = Depends(report_closure)):
    return result


@router.post("/cancellation", response_model=DealEventResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def cancellation(result: DealEventResponse = Depends(report_cancellation)):
    return result


@router.post("/sold-out", response_model=DealEventResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("AGENT", "APPROVER", "ADMIN"))])
async def sold_out(result: DealEventResponse = Depends(report_sold_out)):
    return result
