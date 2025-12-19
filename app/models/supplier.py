
from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base
if TYPE_CHECKING:
    from app.models.product import ProductModel


class SupplierModel(Base):
    __tablename__ = 'suppliers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str]
    phone: Mapped[str]
    address: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    products: Mapped[List["ProductModel"]] = relationship(back_populates="supplier")