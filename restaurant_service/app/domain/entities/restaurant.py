from dataclasses import dataclass, field
from uuid import UUID
from typing import Optional
from datetime import datetime
@dataclass
class Restaurant:
    """
    Domain entity representation for Restaurant 
    """
    id: UUID
    name: str
    address: str
    contact_phone: str
    is_active: bool
    opening_hours: dict
    created_at: datetime = field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None
    updated_at: Optional[datetime] = None
    