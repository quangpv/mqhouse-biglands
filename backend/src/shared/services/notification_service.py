import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.entities.notification import NotificationEntity
from src.data.entities.user import UserRole
from src.data.repositories.notification_repo import NotificationRepo
from src.data.repositories.user_repo import UserRepo
from src.modules.notifications.mapper import entity_to_response
from src.platform.dependencies import get_db
from src.platform.ws_manager import ConnectionManager, get_ws_manager


class NotificationService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        ws_manager: ConnectionManager = Depends(get_ws_manager),
    ):
        self.db = db
        self.ws_manager = ws_manager

    async def notify_admins_and_approvers(
        self,
        *,
        organization_id: uuid.UUID | None,
        title: str,
        body: str | None = None,
        reference_type: str | None = None,
        reference_id: uuid.UUID | None = None,
        event_type: str | None = None,
        actor_name: str | None = None,
        transaction_type: str | None = None,
    ) -> None:
        user_repo = UserRepo(db=self.db)
        notif_repo = NotificationRepo(db=self.db)

        admins = await user_repo.get_by_roles([UserRole.ADMIN])
        approvers: list = []
        if organization_id:
            approvers = await user_repo.get_by_organization_and_roles(
                organization_id, [UserRole.APPROVER],
            )

        seen: set[uuid.UUID] = set()
        for user in admins + approvers:
            if user.id in seen:
                continue
            seen.add(user.id)
            entity = NotificationEntity(
                user_id=user.id,
                title=title,
                body=body,
                reference_type=reference_type,
                reference_id=reference_id,
                event_type=event_type,
                actor_name=actor_name,
                transaction_type=transaction_type,
            )
            await notif_repo.save(entity)

        for user_id in seen:
            await self.ws_manager.send_to_user(str(user_id), {
                "type": "notification_created",
            })

    async def notify_property_owner(
        self,
        *,
        owner_id: uuid.UUID,
        title: str,
        body: str | None = None,
        reference_type: str | None = None,
        reference_id: uuid.UUID | None = None,
        event_type: str | None = None,
        actor_name: str | None = None,
        transaction_type: str | None = None,
    ) -> None:
        notif_repo = NotificationRepo(db=self.db)

        entity = NotificationEntity(
            user_id=owner_id,
            title=title,
            body=body,
            reference_type=reference_type,
            reference_id=reference_id,
            event_type=event_type,
            actor_name=actor_name,
            transaction_type=transaction_type,
        )
        await notif_repo.save(entity)

        await self.ws_manager.send_to_user(str(owner_id), {
            "type": "notification_created",
        })
