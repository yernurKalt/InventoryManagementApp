from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str



class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72, description="Password must be between 8 and 72 characters")


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] | None = None

    model_config = ConfigDict(from_attributes=True)