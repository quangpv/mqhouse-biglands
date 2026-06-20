from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.platform.dependencies import get_db


class Repo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def paginated_list(self, query, page: int = 1, size: int = 20) -> tuple[list, int]:
        count_q = select(func.count()).select_from(query.order_by(None).subquery())
        total_result = await self.db.execute(count_q)
        total = total_result.scalar() or 0
        offset = (page - 1) * size
        result = await self.db.execute(query.offset(offset).limit(size))
        rows = result.scalars().all()
        return list(rows), total
