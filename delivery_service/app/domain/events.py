from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass(frozen=True)
class OrderPaidEvent:
    order_id: UUID
    delivery_address: dict
    restaurant_address: dict
    occurred_at: datetime

@dataclass(frozen=True)
class DeliveryStartedEvent:
    order_id: UUID
    occurred_at: datetime

@dataclass(frozen=True)
class DeliveryCompletedEvent:
    order_id: UUID 
    occurred_at: datetime

@dataclass(frozen=True)
class OrderCancelledEvent:
    order_id: UUID
    occurred_at: datetime