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


# ── NUEVO: PUT – reemplaza todos los campos (hereda validaciones de UserCreate) ──
class UserUpdate(UserCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ana Torres Actualizada",
                    "email": "ana.v2@device.com",
                    "role": "support",
                    "is_active": True,
                }
            ]
        }
    }


# ── NUEVO: PATCH – todos los campos opcionales ──────────────────────────────────
class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip() if v else v

    model_config = {
        "json_schema_extra": {
            "examples": [{"role": "support"}]
        }
    }


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}
