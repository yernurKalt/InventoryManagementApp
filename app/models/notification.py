from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base
if TYPE_CHECKING:
    from app.models.user import UserModel
    from app.models.product import ProductModel


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    type: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    is_read: Mapped[bool] = mapped_column(default=False) 
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user: Mapped["UserModel"] = relationship(back_populates="notifications")
    product: Mapped["ProductModel"] = relationship(back_populates="notifications")