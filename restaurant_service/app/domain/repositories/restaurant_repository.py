from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.domain.entities.restaurant import Restaurant

class RestaurantRepository(ABC):

    @abstractmethod
    async def create(self, restaurant_data: Restaurant) -> Restaurant:
        pass

    @abstractmethod
    async def get_restaurants(self, offset: int, limit: int) -> List[Restaurant]:
        pass

    @abstractmethod
    async def get_by_id(self, restaurant_id: UUID) -> Restaurant | None:
        pass

    @abstractmethod
    async def update(self, id: UUID, **kwargs) -> Restaurant | None:
        pass

    @abstractmethod
    async def delete(self, restaurant_id: UUID) -> bool:
        pass

