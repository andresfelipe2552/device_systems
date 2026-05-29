from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ana Torres",
                    "email": "ana.torres@device.com",
                    "role": "admin",
                    "is_active": True,
                }
            ]
        }
    }


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}
