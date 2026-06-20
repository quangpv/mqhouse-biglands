from math import ceil

from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    data: list
    page: int
    size: int
    total: int
    total_pages: int


async def paginate(
    db: AsyncSession,
    query,
    page: int = 1,
    size: int = 20,
) -> tuple[list, int]:
    count_q = select(func.count()).select_from(query.order_by(None).subquery())
    total_result = await db.execute(count_q)
    total = total_result.scalar() or 0

    offset = (page - 1) * size
    result = await db.execute(query.offset(offset).limit(size))
    rows = result.scalars().all()

    return list(rows), total


def build_paginated_response(data: list, page: int, size: int, total: int) -> PaginatedResponse:
    return PaginatedResponse(
        data=data,
        page=page,
        size=size,
        total=total,
        total_pages=ceil(total / size) if size > 0 else 0,
    )
