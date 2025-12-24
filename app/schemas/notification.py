
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class NotificationBase(BaseModel):
    type: str
    message: str

class NotificationOut(NotificationBase):
    id: int
    user_id: int
    product_id: int
    is_read: bool
    created_at: datetime

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


    model_config = ConfigDict(from_attributes=True)