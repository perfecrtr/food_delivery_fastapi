from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.domain.enums import DeliveryStatusEnum
from app.domain.events import DeliveryStartedEvent, DeliveryCompletedEvent
from app.domain.repositories.courier_repository import CourierRepository
from app.domain.repositories.delivery_repository import DeliveryRepository
from app.domain.services.event_producer import EventProducer

@dataclass(frozen=True)
class UpdateDeliveryStatusCommand:
    delivery_id: UUID
    new_status: DeliveryStatusEnum
    auth_id: int

@dataclass(frozen=True)
class UpdateDeliveryStatusResult:
    delivery_id: UUID
    new_status: DeliveryStatusEnum
    updated_at: Optional[datetime]
    msg: str

class UpdateDeliveryStatusHandler:
    def __init__(
        self,
        courier_repo: CourierRepository,
        delivery_repo: DeliveryRepository,
        producer: EventProducer,
    ) -> None:
        self.courier_repo = courier_repo
        self.delivery_repo = delivery_repo
        self.producer = producer

    async def handle(self, command: UpdateDeliveryStatusCommand) -> UpdateDeliveryStatusResult:
        courier = await self.courier_repo.get_by_auth_id(auth_id=command.auth_id)
        if not courier:
            raise ValueError(f"Courier with auth_id {command.auth_id} not found")

        delivery = await self.delivery_repo.get_by_id(delivery_id=command.delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {command.delivery_id} not found")
        
        if delivery.courier_id != courier.id:
            raise ValueError(f"No permission")
        
        if command.new_status == DeliveryStatusEnum.PICKED_UP:
            delivery.pick_up_by_courier()
        elif command.new_status == DeliveryStatusEnum.DELIVERED:
            courier.complete_delivery()
            delivery.delivered_by_courier()
        else:
            raise ValueError(f"Not such status")

        await self.courier_repo.update(courier=courier)
        updated_delivery = await self.delivery_repo.update(delivery=delivery)

        if updated_delivery.status.value == DeliveryStatusEnum.PICKED_UP:
            event = DeliveryStartedEvent(
                order_id=updated_delivery.order_id,
                occurred_at=updated_delivery.updated_at,
            )
            await self.producer.publish(topic="delivery.started", event=event)
        elif updated_delivery.status.value == DeliveryStatusEnum.DELIVERED:
            event = DeliveryCompletedEvent(
                order_id=updated_delivery.order_id,
                occurred_at=updated_delivery.updated_at,
            )
            await self.producer.publish(topic="delivery.completed", event=event)
        else: 
            raise ValueError(f"No such option")

        return UpdateDeliveryStatusResult(
            delivery_id=updated_delivery.id,
            new_status=updated_delivery.status.value,
            msg="Status successfully updated!",
            updated_at=updated_delivery.updated_at,
        )