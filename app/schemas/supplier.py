
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierOut(SupplierBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)