from dataclasses import dataclass
from uuid import UUID

@dataclass
class MenuCategory:
    """
    Domain entity representation for Menu Category
    """
    id: UUID
    name: str