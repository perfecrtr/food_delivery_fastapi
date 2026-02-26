from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, List

from app.domain.enums import CourierStatusEnum

class RegisterCourierRequest(BaseModel):
    pass

class RegisterCourierResponse(BaseModel):
    id:  UUID4
    auth_id: int
    name: str
    phone: str
    is_active: bool
    status: CourierStatusEnum
    created_at: datetime

class UpdateCourierStatusRequest(BaseModel):
    new_status: CourierStatusEnum

class UpdateCourierStatusResponse(BaseModel):
    id: UUID4
    status: CourierStatusEnum
    msg: str
    updated_at: Optional[datetime]

class GetAvailableCouriersRequest(BaseModel):
    limit: int

class CourierInfo(BaseModel):
    id: UUID4
    name: str
    phone: str
    status: CourierStatusEnum

class GetAvailableCouriersResponse(BaseModel):
    couriers: Optional[List[CourierInfo]]