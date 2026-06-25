from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    serial_number: str = Field(..., min_length=3, max_length=50)
    device_type: str = Field(..., min_length=2, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    is_available: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2024-001",
                "device_type": "laptop",
                "brand": "Lenovo",
                "is_available": True
            }
        }
    )


class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=3, max_length=50)
    device_type: Optional[str] = Field(None, min_length=2, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceBasic(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)
