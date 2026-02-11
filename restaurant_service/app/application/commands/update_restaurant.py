from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from app.domain.repositories.restaurant_repository import RestaurantRepository
from app.domain.entities.restaurant import Restaurant
from app.domain.value_objects import Address

@dataclass
class UpdateRestaurantCommand:
    id: UUID
    name: str
    city: str
    street: str
    house_number: str
    building: str
    floor: str
    contact_phone: str
    schedule: dict
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class UpdateRestaurantHandler:

    def __init__(
        self,
        repo: RestaurantRepository
    ):
        self.repo = repo

    async def handle(self, command: UpdateRestaurantCommand) -> dict:

        address = Address(city=command.city,
                          street=command.street,
                          house_number=command.house_number,
                          building=command.building,
                          floor=command.floor)

        restaurant = {
            'name': command.name,
            'address': address.full_address,
            'contact_phone': command.contact_phone,
            'schedule': command.schedule,
            'is_active': command.is_active,
            'description': command.description,
            'coordinates': command.coordinates,
            'tags': command.tags
        }

        saved_restaurant = await self.repo.update(command.id, **restaurant)

        return {
            'id': saved_restaurant.id,
            'name': command.name,
            'address': address.full_address,
            'contact_phone': command.contact_phone,
            'schedule': command.schedule,
            'is_active': command.is_active,
            'description': command.description,
            'coordinates': command.coordinates,
            'tags': command.tags,
            'msg': "Info updated successfully!"
        }
