from sqlalchemy import select
from app.dao.base import BaseDAO
from app.db.db import async_session_maker
from app.models.notification import NotificationModel


class NotificationsDAO(BaseDAO):
    model = NotificationModel


    @classmethod
    async def read_notification(cls, id: id):
        async with async_session_maker() as session:
            notification = await session.execute(select(NotificationModel).where(NotificationModel.id == id))
            notification = notification.scalar_one_or_none()
            if notification:
                notification.is_read = True
                await session.commit()
                return notification
            else:
                return None

    @classmethod
    async def read_all_notifications_for_user(cls, user_id: int):
        async with async_session_maker() as session:
            notifications = await session.execute(select(NotificationModel).where(NotificationModel.user_id == user_id))
            notifications = notifications.scalars().all()
            if notifications is None:
                return None
            for notification in notifications:
                notification.is_read = True
            await session.commit()
            return notifications

    @classmethod
    async def get_by_dedupe_key(cls, dedupe_key: str):
        async with async_session_maker() as session:
            notification = await session.execute(select(NotificationModel).where(NotificationModel.dedupe_key == dedupe_key))
            notification = notification.scalar_one_or_none()
            return notification