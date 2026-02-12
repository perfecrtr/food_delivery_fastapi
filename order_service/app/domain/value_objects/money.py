from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        
        object.__setattr__(self, 'amount', round(self.amount, 2))

    def __add__(self, other: 'Money') -> 'Money':
        amount = self.amount + other.amount
        return Money(amount=amount)
    
    def __sub__(self, other: 'Money') -> 'Money':
        amount = self.amount - other.amount
        return Money(amount=amount)
    
    def __mul__(self, multiplier: int) -> 'Money':
        amount = self.amount * multiplier
        return Money(amount=amount)