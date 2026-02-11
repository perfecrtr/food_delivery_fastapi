from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from app.domain.repositories.restaurant_repository import RestaurantRepository

@dataclass
class GetRestaurantQuery:
    id: UUID

class GetRestaurantHandler:

    def __init__(
        self,
        repo: RestaurantRepository
    ):
        self.repo = repo

    async def handle(self, query: GetRestaurantQuery) -> Optional[dict]:
        
        restaurant = await self.repo.get_by_id(query.id)

        if not restaurant:
            raise

        return {
            "id": restaurant.id,
            "name": restaurant.name,
            "description": restaurant.description,
            "address": restaurant.address.full_address,
            "coordinates": restaurant.coordinates,
            "contact_phone": str(restaurant.contact_phone),
            "is_active": restaurant.is_active,
            "schedule": restaurant.schedule,
            "tags": restaurant.tags
        }
