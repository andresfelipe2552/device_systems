from sqlalchemy.orm import Session
from sqlalchemy import asc
from typing import Optional
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, RoleEnum


# ─── Crear ────────────────────────────────────────────────────────────────────

def create_user(db: Session, payload: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos."""
    new_user = User(
        name=payload.name,
        email=payload.email,
        role=payload.role.value,
        is_active=payload.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ─── Leer ─────────────────────────────────────────────────────────────────────

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Busca un usuario por su ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca un usuario por su email."""
    return db.query(User).filter(User.email == email).first()


def list_users(
    db: Session,
    role: Optional[RoleEnum] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None,
) -> list[User]:
    """
    Lista usuarios con filtros opcionales.
    - role: filtra por rol (admin, support, user)
    - is_active: filtra por estado activo/inactivo
    - order_by: ordena por 'name' o 'created_at'
    """
    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role.value)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if order_by == "name":
        query = query.order_by(asc(User.name))
    elif order_by == "created_at":
        query = query.order_by(asc(User.created_at))

    return query.all()


# ─── Actualizar completo (PUT) ────────────────────────────────────────────────

def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    """Actualiza todos los campos de un usuario (reemplaza completamente)."""
    user.name = payload.name
    user.email = payload.email
    user.role = payload.role.value
    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return user


# ─── Actualizar parcial (PATCH) ───────────────────────────────────────────────

def patch_user(db: Session, user: User, payload: UserPatch) -> User:
    """Actualiza solo los campos enviados en el payload."""
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field == "role" and value is not None:
            value = value.value  # convierte RoleEnum → str
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


# ─── Eliminar ─────────────────────────────────────────────────────────────────

def delete_user(db: Session, user: User) -> None:
    """Elimina un usuario de la base de datos."""
    db.delete(user)
    db.commit()
