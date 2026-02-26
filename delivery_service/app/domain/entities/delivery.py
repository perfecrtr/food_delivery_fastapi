from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.domain.value_objects import Address, DeliveryStatus
from app.domain.enums import DeliveryStatusEnum

@dataclass
class Delivery:
    id: UUID
    order_id: UUID
    restaurant_address: Address
    delivery_address: Address
    status: DeliveryStatus
    created_at: datetime
    courier_id: Optional[UUID] = None   
    assigned_at: Optional[datetime] = None
    picked_up_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def assign_courier(self, courier_id: UUID) -> None:
        if self.status.value != DeliveryStatusEnum.PENDING and self.courier_id != None:
            raise ValueError(f"Delivery is already assigned")
        self.status = DeliveryStatus(value=DeliveryStatusEnum.ASSIGNED)
        self.courier_id = courier_id
        self.updated_at = datetime.utcnow()
        self.assigned_at = datetime.utcnow()

    def pick_up_by_courier(self) -> None:
        if self.status.value != DeliveryStatusEnum.ASSIGNED:
            raise ValueError(f"Delivery is already picked_up")
        self.status = DeliveryStatus(value=DeliveryStatusEnum.PICKED_UP)
        self.picked_up_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def delivered_by_courier(self) -> None:
        if self.status.value != DeliveryStatusEnum.PICKED_UP:
            raise ValueError(f"Delivery is already delivered")
        self.status = DeliveryStatus(value=DeliveryStatusEnum.DELIVERED)
        self.delivered_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def cancelled(self) -> None:
        if self.status.value == DeliveryStatusEnum.DELIVERED or self.status.value == DeliveryStatusEnum.FAILED:
            raise ValueError(f"Cannot to cancel delivery")
        self.status = DeliveryStatus(value=DeliveryStatusEnum.CANCELLED)
        self.cancelled_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


    
