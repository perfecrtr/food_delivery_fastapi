from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from uuid import UUID

@dataclass
class ValidatedItem:
    dish_id: UUID
    name: str
    price: float
    quantity: int

@dataclass
class ValidationResult:
    restaurant_address: Dict[str, Any]
    is_valid: bool
    validated_items: List[ValidatedItem] 
    errors: List[Dict[str, Any]]

class RestaurantService(ABC):

    @abstractmethod
    async def validate_order_items(
        self, 
        restaurant_id: UUID,
        items: List[Dict[str, Any]]
    ) -> ValidationResult:

        pass