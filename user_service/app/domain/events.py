from dataclasses import dataclass

@dataclass
class UserRegisteredEvent:
    user_id: int
    phone_number: str
    fullname: str