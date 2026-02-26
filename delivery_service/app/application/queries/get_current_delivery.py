from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from app.domain.repositories.courier_repository import CourierRepository
from app.domain.repositories.delivery_repository import DeliveryRepository
from app.domain.entities.delivery import Delivery

@dataclass
class GetCurrentDeliveryQuery:
    auth_id: int

class GetCurrentDeliveryHandler:

    def __init__(
        self,
        courier_repo: CourierRepository,
        delivery_repo: DeliveryRepository,
    ):
        self.courier_repo = courier_repo
        self.delivery_repo = delivery_repo

    async def handle(self, query: GetCurrentDeliveryQuery) -> Optional[Delivery]:

        courier = await self.courier_repo.get_by_auth_id(auth_id=query.auth_id)

        if not courier:
            raise ValueError(f"Courier with auth_id {query.auth_id} not found")

        delivery = await self.delivery_repo.get_current_delivery(courier_id=courier.id)
        
        return delivery