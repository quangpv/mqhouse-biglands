import uuid
from datetime import date, datetime
from decimal import Decimal

from fastapi import Depends
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, selectinload

from src.data.entities.property import Action, DirectionType, PropertyEntity, PropertyStatus
from src.data.entities.property_image import PropertyImageEntity
from src.data.entities.property_transition import PropertyTransitionEntity
from src.data.entities.transition_file import TransitionFileEntity
from src.data.entities.user import UserEntity
from src.platform.dependencies import get_db


class PropertyRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    _BASE_LOAD = (
        joinedload(PropertyEntity.creator),
        joinedload(PropertyEntity.transaction_type),
        joinedload(PropertyEntity.property_type),
        selectinload(PropertyEntity.images).selectinload(PropertyImageEntity.file),
    )

    async def get(self, property_id: uuid.UUID) -> PropertyEntity | None:
        result = await self.db.execute(
            select(PropertyEntity)
            .options(*self._BASE_LOAD)
            .where(PropertyEntity.id == property_id)
        )
        return result.unique().scalar_one_or_none()

    async def save(self, entity: PropertyEntity) -> PropertyEntity:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: PropertyEntity) -> None:
        await self.db.delete(entity)
        await self.db.flush()

    async def search(
        self,
        page: int = 1,
        size: int = 20,
        search: str | None = None,
        transaction_type_ids: list[uuid.UUID] | None = None,
        property_type_ids: list[uuid.UUID] | None = None,
        tags: list[str] | None = None,
        districts: list[str] | None = None,
        wards: list[str] | None = None,
        directions: list[DirectionType] | None = None,
        room_count_from: int | None = None,
        room_count_to: int | None = None,
        area_from: Decimal | None = None,
        area_to: Decimal | None = None,
        width_from: Decimal | None = None,
        width_to: Decimal | None = None,
        price_from: Decimal | None = None,
        price_to: Decimal | None = None,
        statuses: list[PropertyStatus] | None = None,
        is_hot: bool | None = None,
        created_by_id: uuid.UUID | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[PropertyEntity], int]:
        q = select(PropertyEntity).options(*self._BASE_LOAD)

        count_q = select(func.count()).select_from(PropertyEntity)

        if search:
            pattern = f"%{search}%"
            q = q.where(
                or_(
                    PropertyEntity.code.ilike(pattern),
                    PropertyEntity.title.ilike(pattern),
                    PropertyEntity.description.ilike(pattern),
                    PropertyEntity.address.ilike(pattern),
                    PropertyEntity.ward.ilike(pattern),
                    PropertyEntity.district.ilike(pattern),
                )
            )
            count_q = count_q.where(
                or_(
                    PropertyEntity.code.ilike(pattern),
                    PropertyEntity.title.ilike(pattern),
                    PropertyEntity.description.ilike(pattern),
                    PropertyEntity.address.ilike(pattern),
                    PropertyEntity.ward.ilike(pattern),
                    PropertyEntity.district.ilike(pattern),
                )
            )

        if transaction_type_ids:
            q = q.where(PropertyEntity.transaction_type_id.in_(transaction_type_ids))
            count_q = count_q.where(PropertyEntity.transaction_type_id.in_(transaction_type_ids))

        if property_type_ids:
            q = q.where(PropertyEntity.property_type_id.in_(property_type_ids))
            count_q = count_q.where(PropertyEntity.property_type_id.in_(property_type_ids))

        if tags:
            tag_conditions = []
            for tag in tags:
                if tag == "newest":
                    tag_conditions.append(PropertyEntity.created_at >= func.now() - func.make_interval(days=7))
                elif tag == "best_selling":
                    pass
                elif tag == "hot":
                    tag_conditions.append(PropertyEntity.is_hot.is_(True))
            if tag_conditions:
                q = q.where(or_(*tag_conditions))
                count_q = count_q.where(or_(*tag_conditions))

        if districts:
            q = q.where(PropertyEntity.district.in_(districts))
            count_q = count_q.where(PropertyEntity.district.in_(districts))

        if wards:
            q = q.where(PropertyEntity.ward.in_(wards))
            count_q = count_q.where(PropertyEntity.ward.in_(wards))

        if directions:
            q = q.where(PropertyEntity.direction.in_(directions))
            count_q = count_q.where(PropertyEntity.direction.in_(directions))

        if room_count_from is not None:
            q = q.where(PropertyEntity.num_rooms >= room_count_from)
            count_q = count_q.where(PropertyEntity.num_rooms >= room_count_from)
        if room_count_to is not None:
            q = q.where(PropertyEntity.num_rooms <= room_count_to)
            count_q = count_q.where(PropertyEntity.num_rooms <= room_count_to)

        if area_from is not None:
            q = q.where(PropertyEntity.total_area >= area_from)
            count_q = count_q.where(PropertyEntity.total_area >= area_from)
        if area_to is not None:
            q = q.where(PropertyEntity.total_area <= area_to)
            count_q = count_q.where(PropertyEntity.total_area <= area_to)

        if width_from is not None:
            q = q.where(PropertyEntity.area_width >= width_from)
            count_q = count_q.where(PropertyEntity.area_width >= width_from)
        if width_to is not None:
            q = q.where(PropertyEntity.area_width <= width_to)
            count_q = count_q.where(PropertyEntity.area_width <= width_to)

        if price_from is not None:
            q = q.where(PropertyEntity.price >= price_from)
            count_q = count_q.where(PropertyEntity.price >= price_from)
        if price_to is not None:
            q = q.where(PropertyEntity.price <= price_to)
            count_q = count_q.where(PropertyEntity.price <= price_to)

        if statuses:
            q = q.where(PropertyEntity.status.in_(statuses))
            count_q = count_q.where(PropertyEntity.status.in_(statuses))

        if is_hot is not None:
            q = q.where(PropertyEntity.is_hot.is_(is_hot))
            count_q = count_q.where(PropertyEntity.is_hot.is_(is_hot))

        if created_by_id is not None:
            q = q.where(PropertyEntity.created_by_id == created_by_id)
            count_q = count_q.where(PropertyEntity.created_by_id == created_by_id)

        q = q.where(PropertyEntity.deleted_at.is_(None))
        count_q = count_q.where(PropertyEntity.deleted_at.is_(None))

        sort_col = getattr(PropertyEntity, sort_by, PropertyEntity.created_at)
        if sort_order == "asc":
            q = q.order_by(sort_col.asc())
        else:
            q = q.order_by(sort_col.desc())

        total_result = await self.db.execute(count_q)
        total = total_result.scalar() or 0

        offset = (page - 1) * size
        q = q.offset(offset).limit(size)
        result = await self.db.execute(q)
        rows = list(result.unique().scalars().all())

        return rows, total

    async def create_transition(
        self,
        property_id: uuid.UUID,
        from_status: PropertyStatus | None,
        to_status: PropertyStatus,
        action: Action,
        actor_id: uuid.UUID,
        actor_name: str,
        notes: str | None = None,
        customer_name: str | None = None,
        customer_phone: str | None = None,
        contract_date: date | None = None,
        file_ids: list[uuid.UUID] | None = None,
    ) -> PropertyTransitionEntity:
        transition = PropertyTransitionEntity(
            property_id=property_id,
            from_status=from_status,
            to_status=to_status,
            action=action,
            actor_id=actor_id,
            actor_name=actor_name,
            notes=notes,
            customer_name=customer_name,
            customer_phone=customer_phone,
            contract_date=contract_date,
            created_at=datetime.now(),
        )
        if file_ids:
            transition.files = [TransitionFileEntity(file_id=fid) for fid in file_ids]

        self.db.add(transition)
        await self.db.flush()
        await self.db.refresh(transition)
        return transition

    async def get_transitions(self, property_id: uuid.UUID) -> list[PropertyTransitionEntity]:
        result = await self.db.execute(
            select(PropertyTransitionEntity)
            .options(joinedload(PropertyTransitionEntity.files))
            .where(PropertyTransitionEntity.property_id == property_id)
            .order_by(PropertyTransitionEntity.created_at)
        )
        return list(result.unique().scalars().all())

    async def get_user_by_id(self, user_id: uuid.UUID) -> UserEntity | None:
        result = await self.db.execute(select(UserEntity).where(UserEntity.id == user_id))
        return result.scalar_one_or_none()

    async def get_file_ids_in_property(self, property_id: uuid.UUID) -> list[uuid.UUID]:
        result = await self.db.execute(
            select(PropertyImageEntity.file_id).where(PropertyImageEntity.property_id == property_id)
        )
        return list(result.scalars().all())

    async def create_image(self, property_id: uuid.UUID, file_id: uuid.UUID, order: int = 0, is_primary: bool = False) -> PropertyImageEntity:
        image = PropertyImageEntity(
            property_id=property_id,
            file_id=file_id,
            order=order,
            is_primary=is_primary,
        )
        self.db.add(image)
        await self.db.flush()
        await self.db.refresh(image)
        return image

    async def load_images(self, entity: PropertyEntity) -> None:
        result = await self.db.execute(
            select(PropertyImageEntity)
            .where(PropertyImageEntity.property_id == entity.id)
            .options(selectinload(PropertyImageEntity.file))
            .order_by(PropertyImageEntity.order)
        )
        entity.images = list(result.unique().scalars().all())
