from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class Restaurant:
    """
    Domain entity representation for Restaurant 
    """
    id: UUID
    name: str
    description: Optional[str]
    address: str
    coordinates: Optional[dict]
    contact_phone: str
    is_active: bool
    opening_hours: dict
    tags: Optional[list]
    