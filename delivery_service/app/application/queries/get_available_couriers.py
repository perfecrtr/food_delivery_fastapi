from dataclasses import dataclass
from typing import Optional, List

from app.domain.repositories.courier_repository import CourierRepository
from app.domain.entities.courier import Courier

@dataclass
class GetAvailableCouriersQuery:
    limit: int = 10

class GetAvailableCouriersHandler:

    def __init__(
        self,
        repo: CourierRepository,
    ):
        self.repo = repo

    async def handle(self, query: GetAvailableCouriersQuery) -> Optional[List[Courier]]:

        couriers = await self.repo.find_available(limit=query.limit)
        
        if not couriers:
            return None
        
        return couriers