from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services import user_service, loan_service
from app.models.user_model import User

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Requiere autenticación. Límite: 30/min."
)
@limiter.limit("30/minute")
def list_users(
    request: Request,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user)
):
    return user_service.get_all_users(db, search)


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_active_user)):
    return user_service.get_user_by_id(db, user_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario completo")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_active_user)):
    return user_service.update_user(db, user_id, data)


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar usuario parcial")
def patch_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_active_user)):
    return user_service.update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    user_service.delete_user(db, user_id)


@router.get("/{user_id}/loans", response_model=List[LoanDetailResponse], summary="Préstamos de un usuario")
def get_user_loans(user_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_active_user)):
    return loan_service.get_loans_by_user(db, user_id)
