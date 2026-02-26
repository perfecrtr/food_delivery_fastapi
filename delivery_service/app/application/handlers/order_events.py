from uuid import uuid4
from dataclasses import asdict
from datetime import datetime
import asyncio

from app.domain.services.event_producer import EventProducer
from app.domain.events import OrderPaidEvent, OrderCancelledEvent
from app.domain.enums import DeliveryStatusEnum
from app.domain.entities.delivery import Delivery
from app.domain.value_objects import DeliveryStatus, Address
from app.domain.repositories.delivery_repository import DeliveryRepository
from app.domain.repositories.courier_repository import CourierRepository
from app.domain.services.courier_assignment import CourierAssignment

class OrderEventsHandler:
    
    def __init__(
        self,
        delivery_repo: DeliveryRepository,
        courier_repo: CourierRepository,
        courier_assigner: CourierAssignment,
    ) -> None:
        self.delivery_repo = delivery_repo
        self.courier_repo = courier_repo
        self.courier_assigner = courier_assigner

    async def handle_order_paid(self, event: OrderPaidEvent) -> Delivery:
        
        restaurant_address = Address(
            city=event.restaurant_address.get("city", ""),
            street=event.restaurant_address.get("street", ""),
            house_number=event.restaurant_address.get("house_number", ""),
            apartment=event.restaurant_address.get("apartment", ""),
            entrance=event.restaurant_address.get("entrance", ""),
            floor=event.restaurant_address.get("floor", "")
        )

        delivery_address = Address(
            city=event.delivery_address.get("city", ""),
            street=event.delivery_address.get("street", ""),
            house_number=event.delivery_address.get("house_number", ""),
            apartment=event.delivery_address.get("apartment", ""),
            entrance=event.delivery_address.get("entrance", ""),
            floor=event.delivery_address.get("floor", "")
        )

        delivery = Delivery(
            id=uuid4(),
            order_id=event.order_id,
            restaurant_address=restaurant_address,
            delivery_address=delivery_address,
            status = DeliveryStatus(value=DeliveryStatusEnum.PENDING),
            created_at=datetime.utcnow(),
        )

        created_delivery = await self.delivery_repo.create(delivery=delivery)
        
        asyncio.create_task(
            self.courier_assigner.assign_to_delivery(delivery_id=created_delivery.id)
        )

        return created_delivery
    
    async def handle_order_cancelled(self, event: OrderCancelledEvent) -> Delivery:

        delivery = await self.delivery_repo.get_by_order_id(event.order_id)
        courier = await self.courier_repo.get_by_id(delivery.courier_id)

        delivery.cancelled()

        if courier:
            courier.complete_delivery()
            await self.courier_repo.update(courier=courier)

        updated_delivery = await self.delivery_repo.update(delivery=delivery)

        return updated_delivery
