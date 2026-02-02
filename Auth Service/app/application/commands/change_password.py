from dataclasses import dataclass

from app.infrastructure.db.repository import UserRepository
from app.domain.value_objects.password import Password
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.security.password_hasher import BcryptPasswordHasher


@dataclass
class UserChangePasswordCommand:
    phone: str
    old_password: str
    new_password: str

class UserChangePasswordHandler:
    def __init__(self,
                 user_repository : UserRepository,
                 password_hasher : BcryptPasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def handle(self, command : UserChangePasswordCommand):

        old_pass = Password(command.old_password)
        new_pass = Password(command.new_password)
        phone_number = PhoneNumber(command.phone)

        user = await self.user_repository.get_by_phone_number(phone_number)

        if not user:
            raise ValueError("No such user")

        if not self.password_hasher.verify(old_pass, user.hashed_password):
            raise ValueError("Invalid password")

        if new_pass == old_pass:
            raise ValueError("Same password")

        new_password_hash = self.password_hasher.hash(new_pass)
        user.hashed_password = new_password_hash

        await self.user_repository.save(user)

        return {
            "success" : True,
            "message" : "Пароль успешно изменен",
            "user_id" : str(user.id)
        }