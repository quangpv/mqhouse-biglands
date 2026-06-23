import uuid
from decimal import Decimal

from fastapi import Depends
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.data.entities.approval import ApprovalEntity, ApprovalStatus
from src.data.entities.property import PropertyEntity
from src.data.entities.property_image import PropertyImageEntity
from src.data.entities.transaction_type import TransactionTypeEntity
from src.platform.dependencies import get_db


class ApprovalRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    _PROPERTY_LOADS = (
        joinedload(PropertyEntity.creator),
        joinedload(PropertyEntity.transaction_type),
        joinedload(PropertyEntity.property_type),
        joinedload(PropertyEntity.images).joinedload(PropertyImageEntity.file),
    )

    _BASE_LOADS = (
        joinedload(ApprovalEntity.property).options(*_PROPERTY_LOADS),
        joinedload(ApprovalEntity.transition),
        joinedload(ApprovalEntity.decision_transition),
        joinedload(ApprovalEntity.transaction_type),
    )

    async def get(self, approval_id: uuid.UUID) -> ApprovalEntity | None:
        result = await self.db.execute(
            select(ApprovalEntity)
            .options(*self._BASE_LOADS)
            .where(ApprovalEntity.id == approval_id)
        )
        return result.unique().scalar_one_or_none()

    async def save(self, entity: ApprovalEntity) -> ApprovalEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def search(
        self,
        page: int = 1,
        size: int = 20,
        status: ApprovalStatus | None = None,
        transaction_type_ids: list[uuid.UUID] | None = None,
        search: str | None = None,
        property_type_ids: list[uuid.UUID] | None = None,
        districts: list[str] | None = None,
        wards: list[str] | None = None,
        price_from: Decimal | None = None,
        price_to: Decimal | None = None,
        area_from: Decimal | None = None,
        area_to: Decimal | None = None,
        requested_by_id: uuid.UUID | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[ApprovalEntity], int]:
        conditions = []

        if status is not None:
            conditions.append(ApprovalEntity.status == status)
        if transaction_type_ids:
            conditions.append(ApprovalEntity.transaction_type_id.in_(transaction_type_ids))

        needs_property_join = any([
            search, property_type_ids, districts, wards,
            price_from, price_to, area_from, area_to, requested_by_id,
        ])

        count_q = select(func.count()).select_from(ApprovalEntity)
        id_q = select(ApprovalEntity.id).select_from(ApprovalEntity)

        if needs_property_join:
            count_q = count_q.join(ApprovalEntity.property)
            id_q = id_q.join(ApprovalEntity.property)

            if search:
                pattern = f"%{search}%"
                search_cond = or_(
                    PropertyEntity.code.ilike(pattern),
                    PropertyEntity.title.ilike(pattern),
                    PropertyEntity.description.ilike(pattern),
                    PropertyEntity.address.ilike(pattern),
                    PropertyEntity.ward.ilike(pattern),
                    PropertyEntity.district.ilike(pattern),
                )
                conditions.append(search_cond)
            if property_type_ids:
                conditions.append(PropertyEntity.property_type_id.in_(property_type_ids))
            if districts:
                conditions.append(PropertyEntity.district.in_(districts))
            if wards:
                conditions.append(PropertyEntity.ward.in_(wards))
            if price_from is not None:
                conditions.append(PropertyEntity.price >= price_from)
            if price_to is not None:
                conditions.append(PropertyEntity.price <= price_to)
            if area_from is not None:
                conditions.append(PropertyEntity.total_area >= area_from)
            if area_to is not None:
                conditions.append(PropertyEntity.total_area <= area_to)
            if requested_by_id is not None:
                conditions.append(PropertyEntity.created_by_id == requested_by_id)

        count_q = count_q.where(*conditions)
        total_result = await self.db.execute(count_q)
        total = total_result.scalar() or 0

        id_q = id_q.where(*conditions)

        sort_col = getattr(ApprovalEntity, sort_by, ApprovalEntity.created_at)
        if sort_order == "asc":
            id_q = id_q.order_by(sort_col.asc())
        else:
            id_q = id_q.order_by(sort_col.desc())

        offset = (page - 1) * size
        id_q = id_q.offset(offset).limit(size)
        ids_result = await self.db.execute(id_q)
        ids = list(ids_result.scalars().all())

        if not ids:
            return [], total

        data_q = (
            select(ApprovalEntity)
            .options(*self._BASE_LOADS)
            .where(ApprovalEntity.id.in_(ids))
        )
        data_result = await self.db.execute(data_q)
        rows = list(data_result.unique().scalars().all())

        id_order = {str(id_): i for i, id_ in enumerate(ids)}
        rows.sort(key=lambda r: id_order.get(str(r.id), 0))

        return rows, total

    async def count_by_transaction_type(
        self, status: ApprovalStatus | None = None
    ) -> list[tuple[str, int]]:
        q = (
            select(TransactionTypeEntity.code, func.count(ApprovalEntity.id))
            .select_from(ApprovalEntity)
            .join(
                TransactionTypeEntity,
                ApprovalEntity.transaction_type_id == TransactionTypeEntity.id,
            )
        )
        if status is not None:
            q = q.where(ApprovalEntity.status == status)
        q = q.group_by(TransactionTypeEntity.code)
        result = await self.db.execute(q)
        return list(result.tuples().all())
