from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.domain.enums import PaymentStatus, PaymentMethodType
from app.domain.value_objects.money import Money

@dataclass(frozen=True)
class Payment:
    id: UUID
    order_id: UUID
    user_id: int
    restaurant_id: UUID
    amount: Money
    status: PaymentStatus
    payment_method: PaymentMethodType
    created_at: datetime
    updated_at: Optional[datetime] = None