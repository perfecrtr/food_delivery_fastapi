from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from app.domain.repositories.delivery_repository import DeliveryRepository
from app.domain.entities.delivery import Delivery

@dataclass
class GetDeliveryByIdQuery:
    delivery_id: UUID

class GetDeliveryByIdHandler:

    def __init__(
        self,
        repo: DeliveryRepository,
    ):
        self.repo = repo

    async def handle(self, query: GetDeliveryByIdQuery) -> Optional[Delivery]:

        delivery = await self.repo.get_by_id(delivery_id=query.delivery_id)
        
        return delivery