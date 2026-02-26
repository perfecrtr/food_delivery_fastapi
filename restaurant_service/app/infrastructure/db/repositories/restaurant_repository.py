from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.restaurant import Restaurant
from app.domain.repositories.restaurant_repository import RestaurantRepository
from app.domain.value_objects import Address
from app.infrastructure.db.models import RestaurantModel
from app.infrastructure.db.mappers.restaurant_mapper import restaurant_model_to_entity, restaurant_entity_to_model

class SQLAlchemyRestaurantRepository(RestaurantRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, restaurant_data: Restaurant) -> Restaurant:
        model = restaurant_entity_to_model(restaurant_data)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return restaurant_model_to_entity(model)

    async def get_restaurants(self, offset: int, limit: int) -> List[Restaurant]:
        stmt = select(RestaurantModel).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        
        restaurants = [restaurant_model_to_entity(model) for model in models]

        return restaurants if restaurants else []

    async def get_by_id(self, restaurant_id: UUID) -> Restaurant | None:
        stmt = select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()

        return restaurant_model_to_entity(model) if model else None
    
    async def get_restaurant_address(self, restaurant_id: UUID) -> Address | None:
        stmt = select(RestaurantModel.address).where(RestaurantModel.id == restaurant_id)
        result = await self.db.execute(stmt)
        address = result.scalar_one_or_none()

        if not address:
            return None

        return Address.from_model(address_string=address)

    async def update(self, restaurant_id: UUID, **kwargs) -> Restaurant | None:
        stmt = select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        
        await self.db.commit()
        await self.db.refresh(model)
        return restaurant_model_to_entity(model)

    async def delete(self, restaurant_id: UUID) -> bool:
        pass

