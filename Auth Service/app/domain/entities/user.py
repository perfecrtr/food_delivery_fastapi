from dataclasses import dataclass, field
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.password import Password
from app.infrastructure.security.password_hasher import PasswordHasher
from datetime import datetime, timedelta, timezone
from typing import Optional



@dataclass
class User:
    phone_number: PhoneNumber
    hashed_password: str
    id: Optional[int] = None

    @classmethod
    def create(
        cls,
        phone_number: str,
        password: Password,
        password_hasher: PasswordHasher
    ) -> 'User':
        password_hash = password_hasher.hash(password)
        phone_vo = PhoneNumber(value=phone_number)
        return cls(
            id = None,
            phone_number=phone_vo,
            hashed_password=password_hash
        )

    def verify_password(
        self,
        password : str,
        password_hasher: PasswordHasher
    ) -> bool:
        return password_hasher.verify(password, self.hash_password)

    def update_password(
        self,
        new_password : str,
        password_hasher: PasswordHasher
    ) -> None:
        self.hash_password = password_hasher.hash(new_password)