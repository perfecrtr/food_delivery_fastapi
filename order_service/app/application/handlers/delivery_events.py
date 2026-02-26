from uuid import uuid4
from dataclasses import asdict
from datetime import datetime

from app.domain.repositories.order_repository import OrderRepository
from app.domain.events import DeliveryStartedEvent, DeliveryCompletedEvent
from app.domain.enums import OrderStatusEnum
from app.domain.entities.order import Order
from app.domain.value_objects import OrderStatus

class DeliveryEventsHandler:
    
    def __init__(
        self,
        repo: OrderRepository,
    ) -> None:
        
        self.repo = repo

    async def handle_delivery_started(self, event: DeliveryStartedEvent) -> Order:
        order = await self.repo.get_by_id(order_id=event.order_id)
        status = OrderStatus(value=OrderStatusEnum.DELIVERING, changed_at=event.occurred_at)

        order.status = status

        order = await self.repo.update(order_data=order)

        return order

    async def handle_delivery_completed(self, event: DeliveryCompletedEvent) -> Order:
        order = await self.repo.get_by_id(order_id=event.order_id)
        status = OrderStatus(value=OrderStatusEnum.DELIVERED, changed_at=event.occurred_at)

        order.status = status

        order = await self.repo.update(order_data=order)

        return order
