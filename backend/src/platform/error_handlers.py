from fastapi import Request
from fastapi.responses import JSONResponse

from src.shared.errors.exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)


async def api_error_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, UnauthorizedError):
        code = "UNAUTHORIZED"
        if "deactivated" in str(exc.detail).lower():
            code = "ACCOUNT_DEACTIVATED"
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": code, "message": exc.detail},
        )

    for exc_class, code in {
        NotFoundError: "NOT_FOUND",
        ConflictError: "CONFLICT",
        BadRequestError: "VALIDATION_ERROR",
        ForbiddenError: "FORBIDDEN",
    }.items():
        if isinstance(exc, exc_class):
            return JSONResponse(
                status_code=exc.status_code,
                content={"code": code, "message": exc.detail},
            )

    raise exc
