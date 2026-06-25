from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import (
    get_current_active_user, require_admin, require_admin_or_support
)
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.schemas.loan_schema import LoanResponse
from app.services import device_service
from app.models.user_model import User

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get(
    "",
    response_model=List[DeviceResponse],
    summary="Listar dispositivos"
)
def list_devices(
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user)
):
    return device_service.get_all_devices(db, device_type, is_available, brand, search)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID"
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user)
):
    return device_service.get_device_by_id(db, device_id)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Requiere rol admin o support."
)
def create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support)
):
    return device_service.create_device(db, data)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Requiere rol admin o support."
)
def update_device(
    device_id: int,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support)
):
    return device_service.update_device(db, device_id, data)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcial",
    description="Requiere rol admin o support."
)
def patch_device(
    device_id: int,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support)
):
    return device_service.update_device(db, device_id, data)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Requiere rol admin."
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    device_service.delete_device(db, device_id)


@router.get(
    "/{device_id}/loans",
    response_model=List[LoanResponse],
    summary="Préstamos de un dispositivo"
)
def get_device_loans(
    device_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user)
):
    return device_service.get_device_loans(db, device_id)
