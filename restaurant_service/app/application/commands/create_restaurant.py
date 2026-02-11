"""
    Create Restaurant Command and Handler
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from uuid import uuid4
from datetime import datetime
from app.domain.entities.restaurant import Restaurant
from app.domain.repositories.restaurant_repository import RestaurantRepository

@dataclass
class CreateRestaurantCommand:
    name: str
    city: str
    street: str
    house_number: str
    contact_phone: str
    working_schedule: Dict[str, Any]
    building: Optional[str] = None
    floor: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class CreateRestaurantHandler:

    def __init__(
        self,
        repo: RestaurantRepository
    ):
        self.repo= repo

    async def handle(self, command: CreateRestaurantCommand) -> dict:

        restaurant = Restaurant.from_primitives(
            id=uuid4(),
            name=command.name,
            city=command.city,
            street=command.street,
            house_number=command.house_number,
            building=command.building,
            floor=command.floor,
            raw_phone=command.contact_phone,
            working_schedule=command.working_schedule,
            is_active=command.is_active,
            description=command.description,
            coordinates=command.coordinates,
            tags=command.tags
        )

        saved_restaurant = await self.repo.create(restaurant)

        return {
            "id": saved_restaurant.id,
            "msg": "Restaurant successfully created!"
        }