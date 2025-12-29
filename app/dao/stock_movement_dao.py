from sqlalchemy import select
from app.dao.base import BaseDAO
from app.db.db import async_session_maker
from app.models.stock_movement import StockMovementModel


class StockMovementDAO(BaseDAO):
    model = StockMovementModel

    @classmethod
    async def add_model(self, current_user_id, **stock_movement_details):
        new_movement = StockMovementModel(performed_by=current_user_id, **stock_movement_details)
        async with async_session_maker() as session:
            session.add(new_movement)
            await session.commit()
            return new_movement