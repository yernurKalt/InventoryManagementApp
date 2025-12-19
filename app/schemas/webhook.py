import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class WebhookSubscriptionBase(BaseModel):
    name: str
    url: str
    secret: str
    event_type: str
    is_active: bool = True

class WebhookSubscriptionCreate(WebhookSubscriptionBase):
    pass

class WebhookSubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    secret: Optional[str] = None
    event_type: Optional[str] = None
    is_active: Optional[bool] = None

class WebhookSubscriptionOut(WebhookSubscriptionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)