from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from  uuid import UUID
from typing import Optional, List



from app.domain.repositories.delivery_repository import DeliveryRepository
from app.domain.entities.delivery import Delivery
from app.domain.enums import DeliveryStatusEnum
from app.infrastructure.db.mappers.delivery_mapper import delivery_entity_to_model, delivery_model_to_entity
from app.infrastructure.db.models import DeliveryModel

class SQLAlchemyDeliveryRepository(DeliveryRepository):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, delivery_id: UUID) -> Optional[Delivery]:
        stmt = select(DeliveryModel).where(DeliveryModel.id == delivery_id)
        result = await self.db.execute(stmt)
        delivery_model = result.scalar_one_or_none()

        return delivery_model_to_entity(model=delivery_model) if delivery_model else None
    
    async def get_by_order_id(self, order_id: UUID) -> Optional[Delivery]:
        stmt = select(DeliveryModel).where(DeliveryModel.order_id == order_id)
        result = await self.db.execute(stmt)
        delivery_model = result.scalar_one_or_none()

        return delivery_model_to_entity(model=delivery_model) if delivery_model else None
    
    async def get_current_delivery(self, courier_id: UUID) -> Optional[Delivery]:
        stmt = select(DeliveryModel).where(
            DeliveryModel.delivered_at == None,
            DeliveryModel.failed_at == None,
            DeliveryModel.cancelled_at == None,
            DeliveryModel.courier_id == courier_id,
        )
        result = await self.db.execute(stmt)
        delivery_model = result.scalar_one_or_none()

        return delivery_model_to_entity(model=delivery_model) if delivery_model else None

    async def create(self, delivery: Delivery) -> Delivery:
        existing = await self.get_by_id(delivery_id=delivery.id)
        if existing:
            raise ValueError(f"Delivery with {delivery.id} id already existing!")
        delivery_model = delivery_entity_to_model(entity=delivery)
        self.db.add(delivery_model)
        await self.db.commit()
        await self.db.refresh(delivery_model)
        return delivery_model_to_entity(model=delivery_model)
    
    async def update(self, delivery: Delivery) -> Delivery:
        stmt = select(DeliveryModel).where(DeliveryModel.id == delivery.id)
        result = await self.db.execute(stmt)
        delivery_model = result.scalar_one_or_none()

        if not delivery_model:
            raise ValueError(f"Delivery {delivery.id} not found")

        delivery_model.status = delivery.status.value
        delivery_model.courier_id = delivery.courier_id
        delivery_model.assigned_at = delivery.assigned_at
        delivery_model.cancelled_at = delivery.cancelled_at
        delivery_model.delivered_at = delivery.delivered_at
        delivery_model.failed_at = delivery.failed_at
        delivery_model.picked_up_at = delivery.picked_up_at
        delivery_model.updated_at = delivery.updated_at

        await self.db.commit()
        await self.db.refresh(delivery_model)

        return delivery_model_to_entity(delivery_model)