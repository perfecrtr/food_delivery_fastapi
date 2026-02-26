from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from app.domain.entities.courier import Courier

class CourierRepository(ABC):

    @abstractmethod
    async def get_by_id(self, courier_id: UUID) -> Optional[Courier]:
        pass

    @abstractmethod
    async def get_by_auth_id(self, auth_id: int) -> Optional[Courier]:
        pass

    @abstractmethod
    async def create(self, courier: Courier) -> Courier:
        pass

    @abstractmethod
    async def update(self, courier: Courier) -> Courier:
        pass

    @abstractmethod
    async def find_available(self, limit: int = 10) -> List[Courier]:
        pass