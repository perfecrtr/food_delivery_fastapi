from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from app.infrastructure.db.repository import RestaurantRepository
from app.domain.entities.restaurant import Restaurant

@dataclass
class UpdateRestaurantCommand:
    id: UUID
    name: str
    address: str
    contact_phone: str
    opening_hours: dict
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class UpdateRestaurantHandler:

    def __init__(
        self,
        restaurant_repository: RestaurantRepository
    ):
        self.restaurant_repository = restaurant_repository

    async def handle(self, command: UpdateRestaurantCommand) -> dict:

        restaurant = {
            'name': command.name,
            'address': command.address,
            'contact_phone': command.contact_phone,
            'opening_hours': command.opening_hours,
            'is_active': command.is_active,
            'description': command.description,
            'coordinates': command.coordinates,
            'tags': command.tags
        }

        saved_restaurant = await self.restaurant_repository.update(command.id, **restaurant)

        return {
            'id': saved_restaurant.id,
            'name': command.name,
            'address': command.address,
            'contact_phone': command.contact_phone,
            'opening_hours': command.opening_hours,
            'is_active': command.is_active,
            'description': command.description,
            'coordinates': command.coordinates,
            'tags': command.tags,
            'msg': "Info updated successfully!"
        }
