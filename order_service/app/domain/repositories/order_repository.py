from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from app.domain.entities.order import Order

class OrderRepository(ABC):

    @abstractmethod
    async def create(self, order_data: Order) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order:
        pass

    @abstractmethod
    async def get_user_orders(self, user_id: UUID) -> List[Order]:
        pass

    @abstractmethod
    async def update():
        pass
