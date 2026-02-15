"""
    Create order command and handler
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from uuid import uuid4, UUID
from datetime import datetime

from app.domain.entities.order import Order, OrderItem, OrderStatusEnum, OrderStatus
from app.domain.value_objects import Money, Address
from app.domain.repositories.order_repository import OrderRepository
from app.domain.services.restaurant_service import RestaurantService, ValidatedItem, ValidationResult

@dataclass
class CreateOrderCommand:
    restaurant_id: UUID
    user_id: int
    delivery_address: dict
    items: List[Dict[str, Any]]
    

class CreateOrderHandler:

    def __init__(
        self,
        repo: OrderRepository,
        restaurant_service: RestaurantService
    ):
        self.repo = repo
        self.restaurant_service = restaurant_service

    async def handle(self, command: CreateOrderCommand) -> Order:

        validation_result = await self.restaurant_service.validate_order_items(
            restaurant_id=command.restaurant_id,
            items=[
                {"dish_id": item["dish_id"], "quantity": item["quantity"]}
                for item in command.items
            ]
        )

        if not validation_result.is_valid:
            raise ValueError(f"{validation_result}")
        
        order_items = [
            OrderItem(
                id=uuid4(),
                dish_id=item.dish_id,
                name=item.name,
                price=Money(amount=item.price),
                quantity=item.quantity
            )
            for item in validation_result.validated_items
        ]

        delivery_address = Address(
            city=command.delivery_address.get("city", ""),
            street=command.delivery_address.get("street", ""),
            house_number=command.delivery_address.get("house_number", ""),
            apartment=command.delivery_address.get("apartment", ""),
            entrance=command.delivery_address.get("entrance", ""),
            floor=command.delivery_address.get("floor", "")
        )

        order = Order(
            id=uuid4(),
            restaurant_id=command.restaurant_id,
            user_id=command.user_id,
            items=order_items,
            delivery_address=delivery_address,
            total_price=Money(amount=0.0),
            status=OrderStatus(OrderStatusEnum.PENDING)
        )

        saved_order = await self.repo.create(order)

        return saved_order