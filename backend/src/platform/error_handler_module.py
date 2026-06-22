from fastapi import FastAPI

from src.platform.error_handlers import api_error_handler
from src.shared.errors.exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)


def module(app: FastAPI):
    for exc_cls in [NotFoundError, ConflictError, BadRequestError, UnauthorizedError, ForbiddenError]:
        app.add_exception_handler(exc_cls, api_error_handler)
