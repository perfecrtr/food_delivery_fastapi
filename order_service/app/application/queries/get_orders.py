from dataclasses import dataclass
from typing import List

from app.domain.repositories.order_repository import OrderRepository
from app.domain.entities.order_item import OrderItem

@dataclass
class GetOrdersQuery:
    user_id: int
    page: int
    per_page: int

class GetOrdersHandler:

    def __init__(
        self,
        repo: OrderRepository
    ):
        self.repo = repo

    async def handle(self, query: GetOrdersQuery):

        result = await self.repo.get_user_orders(user_id=query.user_id)

        return result