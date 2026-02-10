from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from app.infrastructure.db.repository import DishRepository
from app.domain.entities.dish import Dish

@dataclass
class UpdateDishCommand:
    id: UUID
    restaurant_id: UUID
    price: float
    name: str
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    is_available: Optional[bool] = None

class UpdateDishHandler:

    def __init__(
        self,
        dish_repository: DishRepository
    ):
        self.dish_repository = dish_repository

    async def handle(self, command: UpdateDishCommand) -> dict:

        dish = {
            'restaurant_id': command.restaurant_id,
            'price': command.price,
            'name': command.name,
            'category_id': command.category_id,
            'description': command.description,
            'weight': command.weight,
            'is_available': command.is_available
        }

        saved_dish = await self.dish_repository.update(command.id, **dish)

        return {
            'id': saved_dish.id,
            'restaurant_id': saved_dish.restaurant_id,
            'price': saved_dish.price,
            'name': saved_dish.name,
            'category_id': saved_dish.category_id,
            'description': saved_dish.description,
            'weight': saved_dish.weight,
            'is_available': saved_dish.is_available,
            'msg': "Info updated successfully!"
        }
