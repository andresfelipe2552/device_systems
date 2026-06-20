from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ana Pérez",
                "email": "ana@sena.edu.co",
                "phone": "3001234567"
            }
        }
    }


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}
