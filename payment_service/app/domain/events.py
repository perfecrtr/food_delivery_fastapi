from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from app.domain.enums import PaymentMethodType, PaymentStatus

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
    result: PaymentStatus
    occurred_at: datetime