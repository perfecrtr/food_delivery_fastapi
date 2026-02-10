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
    price: float
    name: str
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    is_available: Optional[bool] = None
    