from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get(
    "",
    response_model=List[LoanResponse],
    summary="Listar préstamos",
    description="Retorna préstamos con filtros opcionales por estado, correo de usuario o tipo de dispositivo."
)
def list_loans(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return loan_service.get_all_loans(db, status, user_email, device_type)


@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    summary="Préstamos con detalle",
    description="Consulta préstamos con información completa del usuario y dispositivo usando joins."
)
def list_loan_details(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return loan_service.get_loan_details(db, status, user_email, device_type)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Obtener préstamo por ID"
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loan_by_id(db, loan_id)


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Crea un préstamo validando que el usuario y el dispositivo existan y que el dispositivo esté disponible."
)
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):
    return loan_service.create_loan(db, data)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Marca el préstamo como devuelto y libera el dispositivo."
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.return_loan(db, loan_id)
