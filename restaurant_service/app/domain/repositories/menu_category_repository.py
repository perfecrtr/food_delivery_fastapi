from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.domain.entities.menu_category import MenuCategory

class MenuCategoryRepository(ABC):

    @abstractmethod
    async def create(self, menu_category_data: MenuCategory) -> MenuCategory:
        pass

    @abstractmethod
    async def get_menu_categories(self, offset: int, limit: int) -> List[MenuCategory]:
        pass






