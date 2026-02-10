"""
    Create Restaurant Command and Handler
"""

from dataclasses import dataclass
from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
from app.domain.entities.dish import Dish
from app.infrastructure.db.repository import DishRepository

@dataclass
class CreateDishCommand:
    restaurant_id: UUID
    price: float
    name: str
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    is_available: Optional[bool] = None

class CreateDishHandler:

    def __init__(
        self,
        dish_repository: DishRepository
    ):
        self.dish_repository = dish_repository

    async def handle(self, command: CreateDishCommand) -> dict:

        dish = Dish(
            id=uuid4(),
            restaurant_id=command.restaurant_id,
            price=command.price,
            name=command.name,
            category_id=command.category_id,
            description=command.description,
            weight=command.weight,
            is_available=command.is_available
        )

        saved_dish = await self.dish_repository.create_dish(dish)

        return {
            "id": saved_dish.id,
            "msg": "Dish successfully created!"
        }