from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Optional, Any, Dict
from datetime import datetime
from app.domain.value_objects import Address, PhoneNumber, WorkingSchedule

@dataclass
class Restaurant:
    """
    Domain entity representation for Restaurant 
    """
    id: UUID
    name: str
    address: Address
    contact_phone: PhoneNumber
    is_active: bool
    schedule: dict
    created_at: datetime
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_primitives(
        cls,
        *,
        id: Optional[UUID] = None,
        name: str,
        city: str,
        street: str,
        house_number: str,
        building: Optional[str] = None,
        floor: Optional[str] = None,
        raw_phone: str,
        working_schedule: Dict[str, Any],
        is_active: bool = True,
        description: Optional[str] = None,
        coordinates: Optional[dict] = None,
        tags: Optional[list] = None,
    ) -> 'Restaurant':
        
        address = Address(city=city, street=street, house_number=house_number, building=building, floor=floor)
        contact_phone = PhoneNumber(raw_phone)
        
        return cls(
            id=id or uuid4(),
            name=name,
            address=address,
            contact_phone=contact_phone,
            schedule=working_schedule,
            is_active=is_active,
            created_at=datetime.utcnow(),
            description=description,
            coordinates=coordinates,
            tags=tags
        )
    