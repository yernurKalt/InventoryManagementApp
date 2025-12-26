
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.schemas.product import ProductinCategoryAndSupplier



class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryOutWithProducts(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    products: List["ProductinCategoryAndSupplier"]

    model_config = ConfigDict(from_attributes=True)