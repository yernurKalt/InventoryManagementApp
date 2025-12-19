import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    sku: str
    category_id: int
    supplier_id: int
    description: Optional[str] = None
    unit_price: float
    reorder_level: int = 0
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    reorder_level: Optional[int] = None
    is_active: Optional[bool] = None

class ProductOut(ProductBase):
    id: int
    current_stock: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)