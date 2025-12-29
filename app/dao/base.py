from datetime import datetime
from typing import Optional
from sqlalchemy import delete, func, select
from app.db.db import async_session_maker
from app.models.product import ProductModel


class BaseDAO():
    model = None
    updt = None

    @classmethod
    def _apply_model_filters(cls, stmt, q: Optional[str]):
        if q:
            stmt = stmt.where(cls.model.name.ilike(f"{q}"))
        return stmt

    @classmethod
    async def count_models(cls, q: Optional[str] = None) -> int:
        stmt = select(func.count()).select_from(cls.model)
        stmt = cls._apply_model_filters(stmt=stmt, q=q)
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            return int(result.scalar_one())

    @classmethod
    async def get_all_models(cls, q: Optional[str] = None):
        async with async_session_maker() as session:
            stmt = select(cls.model)
            stmt = cls._apply_model_filters(stmt=stmt, q=q)
            stmt = stmt.order_by(cls.model.id.asc())
            result = await session.execute(stmt)
            return list(result.scalars().all())


    @classmethod
    async def get_model_by_name(cls, name: str):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.name == name))
            model = result.scalar_one_or_none()
            return model


    @classmethod
    async def get_model_by_id(cls, id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.id == id))
            model = result.scalar_one_or_none()
            return model


    @classmethod
    async def get_model_by_id_with_lock(cls, id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.id == id).with_for_update(of=ProductModel))
            model = result.scalar_one_or_none()
            return model
            

    @classmethod
    async def get_updated_model(cls, id: int, **kwargs):
        
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.id == id))
            model = result.scalar_one_or_none()
            for field, value in kwargs.items():
                if field is None or value is None:
                    continue
                setattr(model, field, value)
            setattr(model, "updated_at", datetime.now())
            await session.commit()
            return model

    @classmethod
    async def add_model(cls, **kwargs):
        async with async_session_maker() as session:
            model = cls.model(**kwargs)
            session.add(model)
            await session.commit()
            return model

    @classmethod
    async def delete_model_from_db(cls, id: id):
        async with async_session_maker() as session:
            await session.execute(delete(cls.model).where(cls.model.id == id))
            await session.commit()