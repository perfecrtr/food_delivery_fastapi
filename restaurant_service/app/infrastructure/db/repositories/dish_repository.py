from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.dish import Dish
from app.domain.repositories.dish_repository import DishRepository
from app.infrastructure.db.models import DishModel
from app.infrastructure.db.mappers.dish_mapper import dish_entity_to_model, dish_model_to_entity

class SQLAlchemyDishRepository(DishRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, dish_data: Dish) -> Dish:
        model = dish_entity_to_model(dish_data)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return dish_model_to_entity(model)

    async def update(self, dish_id: UUID, **kwargs) -> Dish:
        stmt = select(DishModel).where(DishModel.id == dish_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        
        await self.db.commit()
        await self.db.refresh(model)
        return dish_model_to_entity(model)

    async def delete(self, dish_id: UUID) -> bool:
        pass
