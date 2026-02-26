"""
    Create Restaurant Command and Handler
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from uuid import uuid4, UUID
from datetime import datetime
from app.domain.entities.dish import Dish
from app.domain.repositories.menu_repository import MenuRepository
from app.domain.repositories.restaurant_repository import RestaurantRepository

@dataclass
class ValidateOrderCommand:
    restaurant_id: UUID
    items: List[Dict[str, Any]]

@dataclass
class ValidateOrderResult:
    restaurant_address: Dict[str, Any]
    is_valid: bool
    validated_items: List[Dict[str, Any]]
    errors: List[Dict[str, Any]]

class ValidateOrderHandler:

    def __init__(
        self,
        menu_repo: MenuRepository,
        restaurant_repo: RestaurantRepository
    ):
        self.menu_repo = menu_repo
        self.restaurant_repo = restaurant_repo

    async def handle(self, command: ValidateOrderCommand) -> ValidateOrderResult:

        address = await self.restaurant_repo.get_restaurant_address(restaurant_id=command.restaurant_id)
        address_dict = asdict(address)
        result = await self.menu_repo.get_restaurant_menu(restaurant_id=command.restaurant_id)

        if not result:
            return ValidateOrderResult(
                restaurant_address=address_dict,
                is_valid=False,
                validated_items=[],
                errors=[{
                    "code": "RESTAURANT_NOT_FOUND",
                    "message": f"Restaurant {command.restaurant_id} not found or has no menu"
                }]
            )

        menu_dict = {
            item["id"]: item for item in result
        }

        errors = []
        validated_items = []

        for idx, item in enumerate(command.items):
            dish_id = item.get("dish_id")
            quantity = item.get("quantity", 1)

            menu_item = menu_dict.get(dish_id)

            if not menu_item:
                errors.append({
                    "code": "DISH_NOT_FOUND",
                    "message": f"Dish {dish_id} not found in restaurant menu",
                    "dish_id": str(dish_id)
                })

                continue

            validated_items.append({
                    "dish_id": str(dish_id),
                    "name": menu_item['name'],
                    "price": float(menu_item["price"]),
                    "quantity": quantity
                })
        
        if errors:
            return ValidateOrderResult(
                restaurant_address=address_dict,
                is_valid=False,
                validated_items=validated_items,
                errors=errors
            )

        return ValidateOrderResult(
            restaurant_address=address_dict,
            is_valid=True,
            validated_items=validated_items,
            errors=[],
        )