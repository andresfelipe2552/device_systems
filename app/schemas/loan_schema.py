from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.schemas.user_schema import UserBasic
from app.schemas.device_schema import DeviceBasic


class LoanCreate(BaseModel):
    user_id: int
    device_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "device_id": 1
            }
        }
    }


class LoanUpdate(BaseModel):
    status: Optional[str] = None
    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserBasic
    device: DeviceBasic

    model_config = {"from_attributes": True}
