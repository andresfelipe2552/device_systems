from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse, RoleEnum
from app.services import user_service
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/users", tags=["Usuarios"])

CUSTOM_HEADERS = {
    "X-App-Name": "device_systems",
    "X-API-Version": "2.0",
}


def _add_headers(response: Response) -> None:
    for key, value in CUSTOM_HEADERS.items():
        response.headers[key] = value


# ─── GET /users ───────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description=(
        "Retorna la lista de usuarios almacenados en la base de datos. "
        "Soporta filtrado por `role` y `is_active`, y ordenamiento por `name` o `created_at`."
    ),
)
def list_users(
    response: Response,
    db: Session = Depends(get_db),
    role: Optional[RoleEnum] = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo (true/false)"),
    order_by: Optional[str] = Query(None, description="Ordenar por: name, created_at"),
):
    _add_headers(response)
    if order_by and order_by not in ("name", "created_at"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro order_by solo acepta: name, created_at",
        )
    return user_service.list_users(db, role=role, is_active=is_active, order_by=order_by)


# ─── GET /users/{user_id} ─────────────────────────────────────────────────────

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico usando su ID como path parameter.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    _add_headers(response)
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    return user


# ─── POST /users ──────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario en la base de datos. El email debe ser único.",
    responses={
        400: {"description": "Email duplicado"},
        422: {"description": "Error de validación"},
    },
)
def create_user(payload: UserCreate, response: Response, db: Session = Depends(get_db)):
    _add_headers(response)
    if user_service.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el correo '{payload.email}'",
        )
    return user_service.create_user(db, payload)


# ─── PUT /users/{user_id} ─────────────────────────────────────────────────────

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza todos los campos de un usuario existente (actualización completa).",
    responses={
        400: {"description": "Email duplicado en otro usuario"},
        404: {"description": "Usuario no encontrado"},
    },
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    response: Response,
    db: Session = Depends(get_db),
):
    _add_headers(response)
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    # Verificar email duplicado en OTRO usuario
    existing = user_service.get_user_by_email(db, payload.email)
    if existing and existing.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{payload.email}' ya está registrado por otro usuario",
        )
    return user_service.update_user(db, user, payload)


# ─── PATCH /users/{user_id} ───────────────────────────────────────────────────

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Actualiza solo los campos enviados. Los demás campos quedan sin cambios.",
    responses={
        400: {"description": "Email duplicado en otro usuario"},
        404: {"description": "Usuario no encontrado"},
    },
)
def patch_user(
    user_id: int,
    payload: UserPatch,
    response: Response,
    db: Session = Depends(get_db),
):
    _add_headers(response)
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    if payload.email:
        existing = user_service.get_user_by_email(db, payload.email)
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El correo '{payload.email}' ya está registrado por otro usuario",
            )
    return user_service.patch_user(db, user, payload)


# ─── DELETE /users/{user_id} ──────────────────────────────────────────────────

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina permanentemente un usuario de la base de datos.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    user_service.delete_user(db, user)
