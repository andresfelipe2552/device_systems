from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Pérez",
                "email": "ana@sena.edu.co",
                "phone": "3001234567"
            }
        }
    )


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
