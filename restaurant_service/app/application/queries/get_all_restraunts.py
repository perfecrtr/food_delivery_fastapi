from dataclasses import dataclass
from typing import Optional

from app.infrastructure.db.repository import RestaurantRepository

@dataclass
class GetAllRestrauntsQuery:
    page: int = 0
    per_page: int = 10

class GetAllRestrauntsHandler:

    def __init__(
        self,
        restraunt_repository: RestaurantRepository
    ):
        self.restraunt_repository = restraunt_repository

    async def handle(self, query: GetAllRestrauntsQuery) -> Optional[dict]:
        
        offset = query.page * query.per_page

        restaurants = await self.restraunt_repository.get_all(
            skip=offset, 
            limit=query.per_page)

        if not restaurants:
            raise

        return [{
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
        for restaurant in restaurants]