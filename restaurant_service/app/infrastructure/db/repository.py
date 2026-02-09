"""
Repository pattern implementation for database operations
"""

from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.infrastructure.db.database import Base
from app.infrastructure.db.models import RestaurantModel
from app.domain.entities.restaurant import Restaurant

ModelType = TypeVar("ModelType",bound=Base)

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        instance = await self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def delete(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if not instance:
            return False
        
        await self.db.delete(instance)
        await self.db.commit()
        return True
    
    async def exists(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        return instance is not None


class RestaurantRepository(BaseRepository[RestaurantModel]):
    """Repository for Restaurant operations"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(RestaurantModel, db)
    
    async def create_restaurant(self, restaurant: Restaurant) -> RestaurantModel:
        """Create user from domain entity"""
        restaurant_model = RestaurantModel(
            id = restaurant.id,
            name = restaurant.name,
            description = restaurant.description,
            address = restaurant.address,
            coordinates = restaurant.coordinates,
            contact_phone = restaurant.contact_phone,
            is_active = restaurant.is_active,
            opening_hours = restaurant.opening_hours,
            tags=restaurant.tags,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at
        )
        self.db.add(restaurant_model)
        await self.db.commit()
        await self.db.refresh(restaurant_model)
        return restaurant_model