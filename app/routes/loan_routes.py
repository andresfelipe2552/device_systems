from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service
from app.models.user_model import User

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("", response_model=List[LoanResponse], summary="Listar préstamos")
def list_loans(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user)
):
    return loan_service.get_all_loans(db, status, user_email, device_type)


@router.get("/details", response_model=List[LoanDetailResponse], summary="Préstamos con detalle")
def list_loan_details(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support)
):
    return loan_service.get_loan_details(db, status, user_email, device_type)


@router.get("/{loan_id}", response_model=LoanResponse, summary="Obtener préstamo por ID")
def get_loan(loan_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_active_user)):
    return loan_service.get_loan_by_id(db, loan_id)


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Límite: 10/min."
)
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    data: LoanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user)
):
    return loan_service.create_loan(db, data)


@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Devolver dispositivo")
def return_loan(loan_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin_or_support)):
    return loan_service.return_loan(db, loan_id)
