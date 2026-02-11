from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from app.domain.repositories.menu_repository import MenuRepository

@dataclass
class GetRestaurantMenuQuery:
    restaurant_id: UUID

class GetRestaurantMenuHandler:

    def __init__(
        self,
        repo: MenuRepository
    ):
        self.repo = repo

    async def handle(self, query: GetRestaurantMenuQuery) -> list[dict]:
        
        menu_items = await self.repo.get_restaurant_menu(query.restaurant_id)

        if not menu_items:
            raise

        return [{
            "id": item.get("id"),
            "name": item.get("name"),
            "category_name": item.get("category_name"),
            "price": item.get("price"),
            "description": item.get("description"),
            "weight": item.get("weight"),
            "is_available": item.get("is_available")
        }
        for item in menu_items]