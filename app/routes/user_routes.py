from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum

router = APIRouter(prefix="/users", tags=["Usuarios"])

# Base de datos en memoria
_next_id = 1
users_db: list[dict] = [
    {"id": 1, "name": "Carlos Ruiz",    "email": "carlos.ruiz@device.com",   "role": "admin",   "is_active": True},
    {"id": 2, "name": "María López",    "email": "maria.lopez@device.com",   "role": "support", "is_active": True},
    {"id": 3, "name": "Juan Pérez",     "email": "juan.perez@device.com",    "role": "user",    "is_active": False},
    {"id": 4, "name": "Sofía Martínez", "email": "sofia.martinez@device.com","role": "user",    "is_active": True},
]
_next_id = 5

CUSTOM_HEADERS = {
    "X-App-Name": "device_systems",
    "X-API-Version": "1.0",
}


def _add_headers(response: Response) -> None:
    for key, value in CUSTOM_HEADERS.items():
        response.headers[key] = value


# GET /users — lista completa con filtros opcionales
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Se puede filtrar por rol y/o estado activo.",
)
def list_users(
    response: Response,
    role: Optional[RoleEnum] = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo (true/false)"),
):
    _add_headers(response)
    result = users_db.copy()
    if role is not None:
        result = [u for u in result if u["role"] == role.value]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result


# GET /users/{user_id} — buscar por ID
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico usando su ID como path parameter.",
)
def get_user(user_id: int, response: Response):
    _add_headers(response)
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    return user


# POST /users — crear usuario
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Valida datos con Pydantic y evita correos duplicados.",
)
def create_user(payload: UserCreate, response: Response):
    global _next_id
    _add_headers(response)

    # Verificar correo duplicado
    if any(u["email"] == payload.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario con el correo '{payload.email}'",
        )

    new_user = {
        "id": _next_id,
        "name": payload.name,
        "email": payload.email,
        "role": payload.role.value,
        "is_active": payload.is_active,
    }
    users_db.append(new_user)
    _next_id += 1
    return new_user
