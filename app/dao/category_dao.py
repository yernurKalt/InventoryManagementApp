from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.db import async_session_maker
from app.models.category import CategoryModel
from app.schemas.category import CategoryCreate


async def get_all_categories():
    async with async_session_maker() as session:
        result = await session.execute(select(CategoryModel))
        categories = result.scalars().all()
        return categories


async def get_category_by_name(name: str):
    async with async_session_maker() as session:
        result = await session.execute(select(CategoryModel).where(CategoryModel.name == name.lower()))
        category = result.scalar_one_or_none()
        return category


async def add_category(name: str, description: Optional[str] = None):
    async with async_session_maker() as session:
        category = CategoryModel(name=name.lower(), description=description)
        session.add(category)
        await session.commit()
        return category