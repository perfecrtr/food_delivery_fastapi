from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

from app.domain.enums import DeliveryStatusEnum

class DeliveryInfo(BaseModel):
    id: UUID4
    order_id: UUID4
    courier_id: Optional[UUID4]
    restaurant_address: str
    delivery_address: str
    status: DeliveryStatusEnum
    created_at: datetime
    assigned_at: Optional[datetime]
    picked_up_at: Optional[datetime]
    delivered_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    failed_at: Optional[datetime]
    updated_at: Optional[datetime]

class GetDeliveryByIdResponse(BaseModel):
    delivery: Optional[DeliveryInfo]

class GetCurrentDeliveryResponse(BaseModel):
    delivery: Optional[DeliveryInfo]

class UpdateDeliveryStatusRequest(BaseModel):
    new_status: DeliveryStatusEnum

class UpdateDeliveryStatusResponse(BaseModel):
    delivery_id: UUID4
    new_status: DeliveryStatusEnum
    msg: str
    updated_at: datetime
