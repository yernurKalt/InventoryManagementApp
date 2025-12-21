from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import delete, select
from app.db.db import async_session_maker
from app.models.category import CategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate


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


async def get_category_by_id(id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(CategoryModel).where(CategoryModel.id == id))
        category = result.scalar_one_or_none()
        return category


async def get_updated_category(id: int, update: CategoryUpdate):
    
    async with async_session_maker() as session:
        result = await session.execute(select(CategoryModel).where(CategoryModel.id == id))
        category = result.scalar_one_or_none()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category was not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        for field, value in update.model_dump().items():
            if field is None or value is None:
                continue
            setattr(category, field, value)
        setattr(category, "updated_at", datetime.now())
        await session.commit()
        return category

async def add_category(name: str, description: Optional[str] = None):
    async with async_session_maker() as session:
        category = CategoryModel(name=name.lower(), description=description)
        session.add(category)
        await session.commit()
        return category

async def delete_category_from_db(id: id):
    async with async_session_maker() as session:
        await session.execute(delete(CategoryModel).where(CategoryModel.id == id))
        await session.commit()