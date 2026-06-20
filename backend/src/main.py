from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.data.expire_listings import expire_listings
from src.platform.config import settings
from src.platform.scheduler import AppScheduler
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

scheduler = AppScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    scheduler.add_job(expire_listings, trigger="interval", minutes=5, id="expire_listings")
    scheduler.start()
    yield
    scheduler.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    for module_fn in MODULES:
        router = module_fn()
        app.include_router(router)

    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

    return app


app = create_app()
