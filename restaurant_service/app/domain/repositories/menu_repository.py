from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Dict

class MenuRepository(ABC):

    @abstractmethod
    async def get_restaurant_menu(self, restaurant_id: UUID) -> List[Dict]:
        pass