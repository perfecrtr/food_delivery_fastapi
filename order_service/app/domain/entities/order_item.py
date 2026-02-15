from dataclasses import dataclass
from uuid import UUID
from app.domain.value_objects import Money


@dataclass
class OrderItem:
    id: UUID
    dish_id: UUID
    name: str
    price: Money
    quantity: int

    @property
    def total(self) -> Money:
        amount = self.price.amount * self.quantity
        return Money(amount=amount)