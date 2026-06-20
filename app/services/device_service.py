from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def get_all_devices(
    db: Session,
    device_type: str = None,
    is_available: bool = None,
    brand: str = None,
    search: str = None
):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type.ilike(f"%{device_type}%"))
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%")
            )
        )
    return query.all()


def get_device_by_id(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


def create_device(db: Session, data: DeviceCreate):
    existing = db.query(Device).filter(Device.serial_number == data.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    device = Device(**data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(db: Session, device_id: int, data: DeviceUpdate):
    device = get_device_by_id(db, device_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)
    db.delete(device)
    db.commit()


def get_device_loans(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)
    return device.loans
