from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from app.domain.entities.delivery import Delivery

class DeliveryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, delivery_id: UUID) -> Optional[Delivery]:
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> Optional[Delivery]:
        pass

    @abstractmethod
    async def get_current_delivery(self, courier_id: UUID) -> Optional[Delivery]:
        pass

    @abstractmethod
    async def create(self, delivery: Delivery) -> Delivery:
        pass

    @abstractmethod
    async def update(self, delivery: Delivery) -> Delivery:
        pass