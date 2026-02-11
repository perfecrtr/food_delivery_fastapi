from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.domain.entities.dish import Dish

class DishRepository(ABC):

    @abstractmethod
    async def create(self, dish_data: Dish) -> Dish:
        pass

    @abstractmethod
    async def update(self, dish_id: UUID, **kwargs) -> Dish:
        pass

    @abstractmethod
    async def delete(self, dish_id: UUID) -> bool:
        pass

