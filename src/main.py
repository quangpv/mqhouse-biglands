from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.platform.config import settings
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

MODULES: list[Callable[[], Any]] = [
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
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    for module_fn in MODULES:
        router = module_fn()
        app.include_router(router)

    return app


app = create_app()
