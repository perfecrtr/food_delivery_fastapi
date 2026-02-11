from dataclasses import dataclass
import re

@dataclass(frozen=True)
class PhoneNumber:
    """Value Object for Phone Number"""

    value: str

    def __post_init__(self):
        normalized = self._normalize(self.value)
        if not self._is_valid(normalized):
            raise ValueError(f"Invalid phone number format: {self.value}")
        
        object.__setattr__(self,'value', normalized)

    @classmethod
    def _normalize(cls, value: str) -> str:
        normalized = re.sub(r'[\s\-\(\)]', '', value)

        if normalized.startswith('8'):
            normalized = '+375' + normalized[1:]
        elif normalized.startswith('375'):
            normalized = '+' + normalized
        elif not normalized.startswith('+'):
            normalized = '+' + normalized
        
        return normalized
    
    @classmethod
    def _is_valid(cls, value: str) -> str:
        pattern = r'^\+375(29|25|44|33|24)\d{7}$'
        is_valid = re.match(pattern, value)

        return is_valid
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"PhoneNumber('{self.value}')"