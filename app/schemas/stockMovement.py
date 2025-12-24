
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class StockMovementBase(BaseModel):
    product_id: int
    quantity: int
    movement_type: str
    reference: str
    notes: Optional[str] = None

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementOut(StockMovementBase):
    id: int
    perfromed_by: int
    created_at: datetime
    

    model_config = ConfigDict(from_attributes=True)