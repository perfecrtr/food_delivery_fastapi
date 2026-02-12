from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Address:
    city: str
    street: str
    house_number: str
    apartment: Optional[str] = None
    entrance: Optional[str] = None
    floor: Optional[str] = None

    def __post_init__(self):
        if not self.city or not self.street or not self.house_number:
            raise ValueError("City, street and house number are required")
        
    @property
    def full_address(self) -> str:
        parts = [
            f"г. {self.city}",
            f"ул. {self.street}",
            f"д. {self.house_number}"
        ]
        if self.apartment:
            parts.append(f"кв. {self.apartment}")
        if self.entrance:
            parts.append(f"под. {self.entrance}")
        if self.floor:
            parts.append(f"эт. {self.floor}")
        return ", ".join(parts)
