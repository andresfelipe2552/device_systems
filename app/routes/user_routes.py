from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserPatch, RoleEnum
from app.dependencies.user_dependencies import get_user_or_404

router = APIRouter(prefix="/users", tags=["Usuarios"])

# ── Base de datos en memoria (igual que antes) ──────────────────────────────────
users_db: list[dict] = [
    {"id": 1, "name": "Carlos Ruiz",    "email": "carlos.ruiz@device.com",   "role": "admin",   "is_active": True},
    {"id": 2, "name": "María López",    "email": "maria.lopez@device.com",   "role": "support", "is_active": True},
    {"id": 3, "name": "Juan Pérez",     "email": "juan.perez@device.com",    "role": "user",    "is_active": False},
    {"id": 4, "name": "Sofía Martínez", "email": "sofia.martinez@device.com","role": "user",    "is_active": True},
]
_next_id = 5

CUSTOM_HEADERS = {
    "X-App-Name": "device_systems",
    "X-API-Version": "2.0.0",
}


def _add_headers(response: Response) -> None:
    for key, value in CUSTOM_HEADERS.items():
        response.headers[key] = value


# ── GET /users ──────────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Se puede filtrar por rol y/o estado activo.",
    response_description="Lista de usuarios registrados",
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


# ── GET /users/{user_id} ────────────────────────────────────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico usando su ID. Lanza 404 si no existe.",
    response_description="Datos del usuario encontrado",
)
def get_user(response: Response, user: dict = Depends(get_user_or_404)):
    _add_headers(response)
    return user


# ── POST /users ─────────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Evita correos duplicados y valida datos con Pydantic.",
    response_description="Usuario creado exitosamente",
)
def create_user(payload: UserCreate, response: Response):
    global _next_id
    _add_headers(response)

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


# ── PUT /users/{user_id} ────────────────────────────────────────────────────────
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización completa",
    description=(
        "Reemplaza **todos** los campos del usuario. "
        "Lanza 404 si no existe y 409 si el nuevo correo ya está en uso por otro usuario."
    ),
    response_description="Usuario actualizado completamente",
)
def update_user(
    payload: UserUpdate,
    response: Response,
    user: dict = Depends(get_user_or_404),
):
    _add_headers(response)

    # Verificar correo duplicado (excluyendo el propio usuario)
    duplicate = next(
        (u for u in users_db if u["email"] == payload.email and u["id"] != user["id"]),
        None,
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario con el correo '{payload.email}'",
        )

    user["name"] = payload.name
    user["email"] = payload.email
    user["role"] = payload.role.value
    user["is_active"] = payload.is_active
    return user


# ── PATCH /users/{user_id} ──────────────────────────────────────────────────────
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial",
    description=(
        "Modifica **solo los campos enviados**. "
        "Lanza 400 si el body está vacío y 404 si el usuario no existe."
    ),
    response_description="Usuario actualizado parcialmente",
)
def patch_user(
    payload: UserPatch,
    response: Response,
    user: dict = Depends(get_user_or_404),
):
    _add_headers(response)

    changes = payload.model_dump(exclude_none=True)
    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )

    # Verificar correo duplicado si se cambia el email
    if "email" in changes:
        duplicate = next(
            (u for u in users_db if u["email"] == changes["email"] and u["id"] != user["id"]),
            None,
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con el correo '{changes['email']}'",
            )

    # Aplicar solo los campos enviados
    for field, value in changes.items():
        user[field] = value.value if isinstance(value, RoleEnum) else value

    return user


# ── DELETE /users/{user_id} ─────────────────────────────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina el usuario indicado. Lanza 404 si no existe.",
    response_description="Sin contenido – eliminación exitosa",
)
def delete_user(
    response: Response,
    user: dict = Depends(get_user_or_404),
):
    _add_headers(response)
    users_db.remove(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
