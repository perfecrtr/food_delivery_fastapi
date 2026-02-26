from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from app.domain.enums import PaymentMethodType

@dataclass(frozen=True)
class OrderCreatedEvent:
    order_id: UUID
    user_id: int
    restaurant_id: UUID
    total_price: Decimal
    payment_method: PaymentMethodType
    occurred_at: datetime

@dataclass(frozen=True)
class PaymentProcessedEvent:
    payment_id: UUID
    order_id: UUID
    user_id: int
    amount: Decimal
    result: str
    occurred_at: datetime

@dataclass(frozen=True)
class OrderPaidEvent:
    order_id: UUID
    delivery_address: dict
    restaurant_address: dict
    occurred_at: dict

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