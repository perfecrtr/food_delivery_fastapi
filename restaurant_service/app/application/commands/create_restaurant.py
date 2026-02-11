"""
    Create Restaurant Command and Handler
"""

from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from datetime import datetime
from app.domain.entities.restaurant import Restaurant
from app.domain.repositories.restaurant_repository import RestaurantRepository

@dataclass
class CreateRestaurantCommand:
    name: str
    address: str
    contact_phone: str
    opening_hours: dict
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

        restaurant = Restaurant(
            id=uuid4(),
            name=command.name,
            address=command.address,
            contact_phone=command.contact_phone,
            opening_hours=command.opening_hours,
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