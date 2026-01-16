
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class NotificationBase(BaseModel):
    type: str
    message: str
    product_id: int
    user_id: int
    dedupe_key: str

class NotificationOut(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


    model_config = ConfigDict(from_attributes=True)