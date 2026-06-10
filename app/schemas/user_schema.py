from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


# ─── Schema de creación ────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """Schema para crear un usuario nuevo."""

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


# ─── Schema de actualización completa (PUT) ────────────────────────────────────

class UserUpdate(BaseModel):
    """Schema para actualizar todos los campos de un usuario (PUT)."""

    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

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
                    "name": "Ana Torres Actualizada",
                    "email": "ana.torres@device.com",
                    "role": "support",
                    "is_active": True,
                }
            ]
        }
    }


# ─── Schema de actualización parcial (PATCH) ──────────────────────────────────

class UserPatch(BaseModel):
    """Schema para actualizar parcialmente un usuario (PATCH). Todos los campos son opcionales."""

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
            "examples": [
                {
                    "is_active": False,
                }
            ]
        }
    }


# ─── Schema de respuesta ───────────────────────────────────────────────────────

class UserResponse(BaseModel):
    """Schema de respuesta que expone los datos de un usuario al cliente."""

    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
