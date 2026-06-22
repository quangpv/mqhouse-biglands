from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, FastAPI

from src.platform.bootstrap import module as bootstrap_module
from src.platform.config import settings
from src.platform.container import container
from src.platform.scheduler import module as scheduler_module
from src.modules.auth import module as auth_module
from src.modules.users import module as users_module
from src.modules.listings import module as listings_module
from src.modules.listing_images import module as listing_images_module
from src.modules.deal_events import module as deal_events_module
from src.modules.approvals import module as approvals_module
from src.modules.pins import module as pins_module
from src.modules.hot_products import module as hot_products_module
from src.modules.notifications import module as notifications_module
from src.modules.user_settings import module as user_settings_module
from src.modules.organizations import module as organizations_module
from src.modules.geography import module as geography_module
from src.modules.reviews import module as reviews_module

MODULES: list[Callable[..., Any]] = [
    scheduler_module,
    bootstrap_module,
    auth_module,
    users_module,
    listings_module,
    listing_images_module,
    deal_events_module,
    approvals_module,
    pins_module,
    hot_products_module,
    notifications_module,
    user_settings_module,
    organizations_module,
    reviews_module,
    geography_module,
]


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    container[FastAPI] = app

    for module_fn in MODULES:
        result = container.resolve(module_fn)
        if isinstance(result, APIRouter):
            app.include_router(result)

    return app


app = create_app()
