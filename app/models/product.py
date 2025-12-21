from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, null
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base
if TYPE_CHECKING:
    from app.models.category import CategoryModel
    from app.models.supplier import SupplierModel
    from app.models.stock_movement import StockMovementModel
    from app.models.notification import NotificationModel


class ProductModel(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    sku: Mapped[str] = mapped_column(unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    description: Mapped[str]
    unit_price: Mapped[float] = mapped_column(nullable=False)
    current_stock: Mapped[int] = mapped_column(nullable=False, default=0)
    reorder_level: Mapped[int] = mapped_column(nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    category: Mapped["CategoryModel"] = relationship(back_populates="products")
    supplier: Mapped["SupplierModel"] = relationship(back_populates="products")
    stock_movements: Mapped[List["StockMovementModel"]] = relationship(back_populates="product")
    notifications: Mapped[List["NotificationModel"]] = relationship(back_populates="product")