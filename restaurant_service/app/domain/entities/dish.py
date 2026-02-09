from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class Dish:
    """
    Domain entity representation for Dish
    """
    id: UUID
    restaurant_id: UUID
    category_id: Optional[UUID]
    name: str
    description: Optional[str]
    price: float
    weight: Optional[int]
    is_available: bool
    