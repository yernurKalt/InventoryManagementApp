from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, null
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base
if TYPE_CHECKING:
    from app.models.user import UserModel
    from app.models.product import ProductModel

class StockMovementModel(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    movement_type: Mapped[int] = mapped_column(nullable=False)
    reference: Mapped[int] = mapped_column(nullable=True)
    notes: Mapped[int] = mapped_column(nullable=True)
    performed_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user: Mapped['UserModel'] = relationship(back_populates="stock_movements")
    product: Mapped['ProductModel'] = relationship(back_populates="stock_movements")