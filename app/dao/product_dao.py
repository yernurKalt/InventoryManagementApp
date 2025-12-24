from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.db import async_session_maker
from app.models.product import ProductModel
from app.schemas.product import ProductCreate, ProductUpdate
from app.dao.base import BaseDAO


class ProductDAO(BaseDAO):
    model = ProductModel
    updt = ProductUpdate

    @classmethod
    async def find_product_by_sku(cls, sku: str):
        async with async_session_maker() as session:
            result = await session.execute(select(ProductModel).where(ProductModel.sku == sku))
            product = result.scalar_one_or_none()
            return product

    @classmethod
    async def output_product_addition(cls, product: ProductModel):
        stmt = select(ProductModel).options(
        selectinload(ProductModel.category),
        selectinload(ProductModel.supplier)
    ).where(ProductModel.id == product.id)
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            result = result.scalar_one_or_none()
            return result 