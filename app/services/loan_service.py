from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from fastapi import HTTPException
from datetime import datetime, timezone

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse
from app.schemas.user_schema import UserBasic
from app.schemas.device_schema import DeviceBasic


def get_all_loans(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None
):
    query = db.query(Loan).join(User).join(Device)
    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type.ilike(f"%{device_type}%"))
    return query.all()


def get_loan_by_id(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan


def create_loan(db: Session, data: LoanCreate):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    device = db.query(Device).filter(Device.id == data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not device.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no está disponible")

    loan = Loan(user_id=data.user_id, device_id=data.device_id, status="active")
    device.is_available = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int):
    loan = get_loan_by_id(db, loan_id)

    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="El préstamo ya fue devuelto")

    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)
    loan.device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan


def get_loan_details(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None
):
    query = db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    ).join(User).join(Device)

    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type.ilike(f"%{device_type}%"))

    loans = query.all()
    result = []
    for loan in loans:
        result.append(LoanDetailResponse(
            loan_id=loan.id,
            status=loan.status,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            user=UserBasic.model_validate(loan.user),
            device=DeviceBasic.model_validate(loan.device)
        ))
    return result


def get_loans_by_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    loans = db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    ).filter(Loan.user_id == user_id).all()
    result = []
    for loan in loans:
        result.append(LoanDetailResponse(
            loan_id=loan.id,
            status=loan.status,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            user=UserBasic.model_validate(loan.user),
            device=DeviceBasic.model_validate(loan.device)
        ))
    return result
