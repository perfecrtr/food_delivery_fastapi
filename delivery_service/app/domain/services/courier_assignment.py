from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from dataclasses import dataclass

@dataclass
class AssignmentResult:
    success: bool
    delivery_id: Optional[UUID] = None
    courier_id: Optional[UUID] = None
    message: str = ""

class CourierAssignment(ABC):

    @abstractmethod
    async def assign_to_delivery(self, delivery_id: UUID) -> AssignmentResult:
        pass