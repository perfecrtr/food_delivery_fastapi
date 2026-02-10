from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from app.infrastructure.db.repository import DishRepository

@dataclass
class GetRestaurantMenuQuery:
    restaurant_id: UUID

class GetRestaurantMenuHandler:

    def __init__(
        self,
        dish_repository: DishRepository
    ):
        self.dish_repository = dish_repository

    async def handle(self, query: GetRestaurantMenuQuery) -> list[dict]:
        
        menu_items = await self.dish_repository.get_menu_by_restaurant_id(query.restaurant_id)

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