from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base
if TYPE_CHECKING:
    from app.models.product import ProductModel


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    products: Mapped[List["ProductModel"]] = relationship(back_populates="category")