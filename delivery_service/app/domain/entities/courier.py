from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.domain.value_objects import CourierStatus
from app.domain.enums import CourierStatusEnum

@dataclass
class Courier:
    id: UUID
    auth_id: int
    name: str
    phone: str
    is_active: bool
    status: CourierStatus
    created_at: datetime 
    updated_at: Optional[datetime] = None

    
    def __post_init__(self):
        if not self.name or len(self.name) < 2:
            raise ValueError("Name must be at least 2 characters")
        
        if not self.phone:
            raise ValueError("Phone is required")
        
    def go_online(self) -> None:
        if self.status.value != CourierStatusEnum.OFFLINE:
            raise ValueError(f"Cannot go online from status {self.status.value}")
        
        self.status = CourierStatus(
            value=CourierStatusEnum.AVAILABLE,
            changed_at=datetime.utcnow()
        )
        self.updated_at = datetime.utcnow()

    def go_offline(self) -> None:
        if self.status.value == CourierStatusEnum.BUSY:
            raise ValueError("Cannot go offline while busy with delivery")
        
        self.status = CourierStatus(
            value=CourierStatusEnum.OFFLINE,
            changed_at=datetime.utcnow()
        )
        self.updated_at = datetime.utcnow()

    def take_break(self) -> None:
        if self.status.value != CourierStatusEnum.AVAILABLE:
            raise ValueError(f"Cannot take break from status {self.status.value}")
        self.status = CourierStatus(value=CourierStatusEnum.ON_BREAK)
        self.updated_at = datetime.utcnow()
    
    def end_break(self) -> None:
        if self.status.value != CourierStatusEnum.ON_BREAK:
            raise ValueError(f"Cannot end break from status {self.status.value}")
        self.status = CourierStatus(value=CourierStatusEnum.AVAILABLE)
        self.updated_at = datetime.utcnow()

    def assign_to_delivery(self) -> None:
        if self.status.value != CourierStatusEnum.AVAILABLE:
            raise ValueError(f"Courier is not available: {self.status.value}")
        
        self.status = CourierStatus(
            value=CourierStatusEnum.BUSY,
            changed_at=datetime.utcnow()
        )
        self.updated_at = datetime.utcnow()

    def complete_delivery(self) -> None:
        self.status = CourierStatus(
            value=CourierStatusEnum.AVAILABLE,
            changed_at=datetime.utcnow()
        )
        self.updated_at = datetime.utcnow()

    @property
    def is_available(self) -> bool:
        return (
            self.is_active and 
            self.status.value == CourierStatusEnum.AVAILABLE
        )
    
    
        


