from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base
from app.models.stock_movement import StockMovementModel
if TYPE_CHECKING:

    from app.models.notification import NotificationModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    stock_movements: Mapped[List["StockMovementModel"]] = relationship(back_populates="user", lazy="selectin")
    notifications: Mapped[List["NotificationModel"]] = relationship(back_populates="user", lazy="selectin")
     