from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class Address:
    city: str
    street: str
    house_number: str
    building: Optional[str] = None
    floor: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "city", self.city.strip())
        object.__setattr__(self, "street", self.street.strip())
        object.__setattr__(self, "house_number", self.house_number.strip())

        if not self.city:
            raise ValueError("City cannot be empty")
        if not self.street:
            raise ValueError("Street cannot be empty")
        if not self.house_number:
            raise ValueError("House number cannot be empty")

    @property
    def full_address(self) -> str:
        parts = [f"г. {self.city}", f"ул. {self.street}", f"д. {self.house_number}"]
        if self.building:
            parts.append(f"корп. {self.building}")
        if self.floor:
            parts.append(f"этаж {self.floor}")
        return ", ".join(parts)
    
    @classmethod
    def from_model(cls, address_string: str) -> 'Address':
        address_string = address_string.strip()
        
        parts = [part.strip() for part in address_string.split(',')]
        
        city = None
        street = None
        house_number = None
        building = None
        floor = None
        
        for part in parts:
            part_lower = part.lower()
            
            if part_lower.startswith('г.') or part_lower.startswith('г '):
                city = re.sub(r'^г\.?\s*', '', part, flags=re.IGNORECASE).strip()
            
            elif part_lower.startswith('ул.') or part_lower.startswith('ул '):
                street = re.sub(r'^ул\.?\s*', '', part, flags=re.IGNORECASE).strip()
            
            elif part_lower.startswith('д.') or part_lower.startswith('д '):
                house_number = re.sub(r'^д\.?\s*', '', part, flags=re.IGNORECASE).strip()
            
            elif any(part_lower.startswith(x) for x in ['корп.', 'корпус', 'корп']):
                building = re.sub(r'^(корп\.|корпус|корп)\s*', '', part, flags=re.IGNORECASE).strip()
            
            elif any(part_lower.startswith(x) for x in ['этаж', 'эт.']):
                floor = re.sub(r'^(этаж|эт\.)\s*', '', part, flags=re.IGNORECASE).strip()
        
        return cls(
            city=city,
            street=street,
            house_number=house_number,
            building=building,
            floor=floor
        )