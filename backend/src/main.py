from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, FastAPI

from src.modules.auth import module as auth_module
from src.modules.files import module as files_module
from src.modules.geography import module as geography_module
from src.modules.transaction_types import module as transaction_types_module
from src.modules.users import module as users_module
from src.modules.property_types import module as property_types_module
from src.modules.organizations import module as organizations_module
from src.modules.ws import module as ws_module
from src.platform.bootstrap import module as bootstrap_module
from src.platform.config import settings
from src.platform.container import container
from src.platform.error_handler_module import module as error_handler_module
from src.platform.scheduler import module as scheduler_module

MODULES: list[Callable[..., Any]] = [
    error_handler_module,
    scheduler_module,
    bootstrap_module,
    auth_module,
    files_module,
    geography_module,
    transaction_types_module,
    property_types_module,
    organizations_module,
    users_module,
    ws_module,
]


def create_app(api_prefix: str = "/api/v1") -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    container[FastAPI] = app

    for module_fn in MODULES:
        result = container.resolve(module_fn)
        if isinstance(result, APIRouter):
            app.include_router(result, prefix=api_prefix)

    return app


app = create_app()
