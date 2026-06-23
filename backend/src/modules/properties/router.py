from fastapi import APIRouter, Depends

from src.modules.properties.facades.cancel_property import cancel_property
from src.modules.properties.facades.complete_property import complete_property
from src.modules.properties.facades.create_property import create_property
from src.modules.properties.facades.delete_property import delete_property
from src.modules.properties.facades.deposit_property import deposit_property
from src.modules.properties.facades.get_property import get_property
from src.modules.properties.facades.get_status_logs import get_status_logs
from src.modules.properties.facades.list_properties import list_properties
from src.modules.properties.facades.soldout_property import soldout_property
from src.modules.properties.facades.submit_property import submit_property
from src.modules.properties.facades.update_property import update_property
from src.modules.properties.facades.withdraw_property import withdraw_property
from src.modules.properties.schemas import (
    PropertyListResponse,
    PropertyResponse,
    PropertyTransitionListResponse,
)
from src.platform.auth import require_auth

router = APIRouter(prefix="/properties", tags=["Properties"])
router.dependencies = [Depends(require_auth)]


router.add_api_route("", endpoint=create_property, methods=["POST"], response_model=PropertyResponse)
router.add_api_route("", endpoint=list_properties, methods=["GET"], response_model=PropertyListResponse)
router.add_api_route("/{property_id}", endpoint=get_property, methods=["GET"], response_model=PropertyResponse)
router.add_api_route("/{property_id}", endpoint=update_property, methods=["PUT"], response_model=PropertyResponse)
router.add_api_route("/{property_id}", endpoint=delete_property, methods=["DELETE"], response_model=None, status_code=204)
router.add_api_route("/{property_id}/transitions/submit", endpoint=submit_property, methods=["POST"], response_model=PropertyResponse)
router.add_api_route("/{property_id}/transitions/withdraw", endpoint=withdraw_property, methods=["POST"], response_model=PropertyResponse)
router.add_api_route("/{property_id}/transitions/deposit", endpoint=deposit_property, methods=["POST"], response_model=PropertyResponse)
router.add_api_route("/{property_id}/transitions/soldout", endpoint=soldout_property, methods=["POST"], response_model=PropertyResponse)
router.add_api_route("/{property_id}/transitions/cancel", endpoint=cancel_property, methods=["POST"], response_model=PropertyResponse)
router.add_api_route("/{property_id}/transitions/complete", endpoint=complete_property, methods=["POST"], response_model=PropertyResponse)
router.add_api_route("/{property_id}/status-logs", endpoint=get_status_logs, methods=["GET"], response_model=PropertyTransitionListResponse)
