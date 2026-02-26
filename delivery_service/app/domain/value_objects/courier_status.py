from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import CourierStatusEnum

@dataclass(frozen=True)
class CourierStatus:
    value: CourierStatusEnum
    changed_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not isinstance(self.value, CourierStatusEnum):
            raise ValueError("Status must be CourierStatusEnum")