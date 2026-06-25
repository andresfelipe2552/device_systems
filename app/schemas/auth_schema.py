import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

ALLOWED_ROLES = {"admin", "support", "user"}


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre completo")
    email: EmailStr = Field(..., description="Correo electrónico único")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono opcional")
    password: str = Field(..., min_length=8, description="Contraseña segura")
    role: str = Field(default="user", description="Rol: admin, support o user")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contraseña no puede contener espacios")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe tener al menos una minúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ALLOWED_ROLES:
            raise ValueError(f"Rol no permitido. Use: {', '.join(ALLOWED_ROLES)}")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Pérez",
                "email": "ana@sena.edu.co",
                "phone": "3001234567",
                "password": "Segura123",
                "role": "user"
            }
        }
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico")
    password: str = Field(..., description="Contraseña")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "ana@sena.edu.co",
                "password": "Segura123"
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class UserMeResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
