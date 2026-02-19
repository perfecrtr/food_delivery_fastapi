from uuid import uuid4
from datetime import datetime

from app.domain.repositories.order_repository import OrderRepository
from app.domain.services.event_producer import EventProducer
from app.domain.events import PaymentProcessedEvent, OrderPaidEvent
from app.domain.enums import OrderStatusEnum
from app.domain.entities.order import Order
from app.domain.value_objects import OrderStatus

class PaymentEventsHandler:
    
    def __init__(
        self,
        repo: OrderRepository,
        event_producer: EventProducer
    ) -> None:
        
        self.repo = repo
        self.event_producer = event_producer

    async def handle_payment_processed(self, event: PaymentProcessedEvent) -> Order:
        order = await self.repo.get_by_id(order_id=event.order_id)

        if event.result == "completed":
            status = OrderStatus(value=OrderStatusEnum.PAID, changed_at=event.occurred_at)
            order_paid_event = OrderPaidEvent(
                order_id=order.id,
                delivery_address=order.delivery_address.full_address,
                user_id=order.user_id,
                occurred_at=event.occurred_at
            )
            await self.event_producer.publish(topic="order.paid", event=order_paid_event)
        else: 
            status = OrderStatus(value=OrderStatusEnum.FAILED, changed_at=event.occurred_at)

        order.status = status

        order = await self.repo.update(order_data=order)

        return order 
