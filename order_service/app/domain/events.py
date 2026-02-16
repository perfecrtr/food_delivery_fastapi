from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from datetime import datetime

@dataclass(frozen=True)
class OrderCreatedEvent:
    order_id: UUID
    user_id: int
    restaurant_id: UUID
    total_price: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class PaymentSuccededEvent:
    payment_id: UUID
    order_id: UUID
    user_id: int
    amount: Decimal
    occurred_at: datetime