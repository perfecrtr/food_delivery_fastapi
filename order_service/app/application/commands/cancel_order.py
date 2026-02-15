from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from app.domain.repositories.order_repository import OrderRepository

@dataclass
class CancelOrderCommand:
    order_id: UUID
    user_id: int

@dataclass
class CancelOrderResult:
    order_id: UUID
    cancelled_at: datetime
    message: str = "Order cancelled successfully"

class CancelOrderHandler:

    def __init__(
        self,
        repo: OrderRepository
    ):
        self.repo = repo

    async def handle(self, command: CancelOrderCommand):

        order = await self.repo.get_by_id(order_id=command.order_id)

        if not order:
            raise ValueError(f"Order {command.order_id} not found")
        
        if order.user_id != command.user_id:
            raise PermissionError("PermissionError")
        
        try:
            order.cancel()
        except ValueError as e:
            raise ValueError(str(e))
        
        updated_order = await self.repo.update(order)

        return CancelOrderResult(
            order_id=updated_order.id,
            cancelled_at=updated_order.cancelled_at
        )