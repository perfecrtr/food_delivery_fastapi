from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from app.infrastructure.db.repository import RestaurantRepository

@dataclass
class GetRestaurantQuery:
    id: UUID

class GetRestaurantHandler:

    def __init__(
        self,
        restraunt_repository: RestaurantRepository
    ):
        self.restraunt_repository = restraunt_repository

    async def handle(self, query: GetRestaurantQuery) -> Optional[dict]:
        
        restaurant = await self.restraunt_repository.get_by_id(query.id)

        if not restaurant:
            raise

        return {
            "id": restaurant.id,
            "name": restaurant.name,
            "description": restaurant.description,
            "address": restaurant.address,
            "coordinates": restaurant.coordinates,
            "contact_phone": restaurant.contact_phone,
            "is_active": restaurant.is_active,
            "opening_hours": restaurant.opening_hours,
            "tags": restaurant.tags
        }
