from dataclasses import dataclass
from typing import Optional

from app.domain.repositories.restaurant_repository import RestaurantRepository

@dataclass
class GetAllRestrauntsQuery:
    page: int = 0
    per_page: int = 10

class GetAllRestrauntsHandler:

    def __init__(
        self,
        repo: RestaurantRepository
    ):
        self.repo = repo

    async def handle(self, query: GetAllRestrauntsQuery) -> Optional[dict]:
        
        offset = query.page * query.per_page

        restaurants = await self.repo.get_restaurants(
            offset=offset, 
            limit=query.per_page)

        if not restaurants:
            raise

        return [{
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
        for restaurant in restaurants]