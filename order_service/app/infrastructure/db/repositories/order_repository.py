from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List
from datetime import datetime

from app.domain.repositories.order_repository import OrderRepository
from app.domain.entities.order import Order, OrderItem

from app.infrastructure.db.models import OrderItemModel, OrderModel
from app.infrastructure.db.mappers.order_item_mapper import order_item_entity_to_model, order_item_model_to_entity
from app.infrastructure.db.mappers.order_mapper import order_entity_to_model, order_model_to_entity


class SQLAlchemyOrderRepository(OrderRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order_data: Order) -> Order:
        order_model = order_entity_to_model(entity=order_data)

        self.db.add(order_model)
        await self.db.flush()

        for item in order_data.items:
            item_model = order_item_entity_to_model(entity=item, order_id=order_model.id)
            self.db.add(item_model)

        await self.db.commit()
        
        return await self.get_by_id(order_id=order_model.id) 
    
    async def get_by_id(self, order_id: UUID) -> Order:
        stmt = (
            select(OrderModel)
            .where(OrderModel.id == order_id)
            .options(selectinload(OrderModel.items))
        )

        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None
        
        return order_model_to_entity(model=model, include_items=True)

    async def get_user_orders(self, user_id: int) -> List[Order]:
        stmt = (
            select(OrderModel)
            .options(selectinload(OrderModel.items))
            .where(OrderModel.user_id == user_id,
                   OrderModel.delivered_at.is_(None),
                   OrderModel.cancelled_at.is_(None)
            )
            .order_by(OrderModel.created_at.desc())
        )

        result = await self.db.execute(stmt)
        models = result.scalars().all()

        return [order_model_to_entity(model) for model in models]

    async def update(self, order_data: Order) -> Order:
        stmt = (
            select(OrderModel)
            .where(OrderModel.id == order_data.id)
            .options(selectinload(OrderModel.items))
        )
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            raise ValueError(f"Order {order_data.id} not found")
        
        model.status = order_data.status.value
        model.delivered_at = order_data.delivered_at
        model.cancelled_at = order_data.cancelled_at
        model.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(model)

        return order_model_to_entity(model, include_items=True)
