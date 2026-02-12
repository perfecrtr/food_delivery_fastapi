from dataclasses import dataclass, field
from datetime import datetime
from app.domain.enums import OrderStatusEnum

@dataclass(frozen=True)
class OrderStatus:
    value: OrderStatusEnum
    changed_at: datetime = field(default_factory=datetime.utcnow)

    def can_transition_to(self, new_stats: 'OrderStatus') -> bool:
        transitions = {
            OrderStatusEnum.PENDING: [OrderStatusEnum.PAID, OrderStatusEnum.CANCELLED],
            OrderStatusEnum.PAID: [OrderStatusEnum.DELIVERING, OrderStatusEnum.CANCELLED],
            OrderStatusEnum.DELIVERING: [OrderStatusEnum.DELIVERED, OrderStatusEnum.CANCELLED],
            OrderStatusEnum.DELIVERED: [],
            OrderStatusEnum.CANCELLED: []
        }
        return new_stats.value in transitions.get(self.value, [])