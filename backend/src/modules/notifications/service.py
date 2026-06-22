from uuid import UUID

from fastapi import Depends

from src.data.entities.notification import ReferenceType
from src.data.repositories.notification_repo import NotificationRepo
from src.modules.notifications.mapper import notification_to_response
from src.platform.ws_manager import ConnectionManager, get_ws_manager


class NotificationService:
    def __init__(
        self,
        repo: NotificationRepo = Depends(NotificationRepo),
        ws_manager: ConnectionManager = Depends(get_ws_manager),
    ):
        self.repo = repo
        self.ws_manager = ws_manager

    async def send(
        self,
        user_id: UUID | str,
        event_type: str,
        title: str,
        body: str,
        reference_type: ReferenceType | None = None,
        reference_id: UUID | None = None,
        actor_name: str | None = None,
        transaction_type: str | None = None,
    ):
        notification = await self.repo.send(
            user_id=user_id,
            event_type=event_type,
            title=title,
            body=body,
            reference_type=reference_type,
            reference_id=reference_id,
            actor_name=actor_name,
            transaction_type=transaction_type,
        )
        if notification:
            try:
                data = notification_to_response(notification).model_dump(mode="json")
                await self.ws_manager.send_to_user(str(user_id), {
                    "type": "notification_created",
                    "data": data,
                })
            except Exception:
                pass
        return notification
