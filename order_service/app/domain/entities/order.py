from dataclasses import dataclass, field
from uuid import UUID
from typing import List, Optional
from datetime import datetime

from app.domain.entities.order_item import OrderItem
from app.domain.value_objects import Money, Address, OrderStatus
from app.domain.enums import OrderStatusEnum

@dataclass
class Order:
    id: UUID
    restaurant_id: UUID
    user_id: int
    items: List[OrderItem]
    delivery_address: Address
    restaurant_address: Address
    total_price: Money
    status: OrderStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self._recalculate_total()

    def _recalculate_total(self):
        total = sum(float(item.total.amount) for item in self.items)
        self.total_price = Money(amount=total)

    def add_item(self, item: OrderItem):
        self.items.append(item)
        self._recalculate_total()
        self.updated_at = datetime.utcnow()

    def remove_item(self, item_id: UUID):
        self.items = [i for i in self.items if i.id != item_id]
        self._recalculate_total()
        self.updated_at = datetime.utcnow()

    def confirm_payment(self):
        if self.status.value != OrderStatusEnum.PENDING:
            raise ValueError("Only pending orders can be paid")
        self.status = OrderStatus(OrderStatusEnum.PAID)
        self.updated_at = datetime.utcnow()
    
    def assign_delivery(self):
        if self.status.value != OrderStatusEnum.PAID:
            raise ValueError("Only paid orders can be assigned for delivery")
        self.status = OrderStatus(OrderStatusEnum.DELIVERING)
        self.updated_at = datetime.utcnow()

    def complete_delivery(self):
        self.status = OrderStatus(OrderStatusEnum.DELIVERED)
        self.delivered_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def cancel(self):
        if self.status.value in [OrderStatusEnum.DELIVERED, OrderStatusEnum.CANCELLED]:
            raise ValueError(f"Cannot cancel order in status {self.status.value}")
        self.status = OrderStatus(OrderStatusEnum.CANCELLED)
        self.cancelled_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()