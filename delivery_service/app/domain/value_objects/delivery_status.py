from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import DeliveryStatusEnum

@dataclass(frozen=True)
class DeliveryStatus:
    value: DeliveryStatusEnum
    changed_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not isinstance(self.value, DeliveryStatusEnum):
            raise ValueError("Status must be DeliveryStatusEnum")
