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

        old_pass = Password(value=command.old_password)
        new_pass = Password(value=command.new_password)
        phone_number = PhoneNumber(value=command.phone)

        user = await self.user_repository.get_by_phone_number(str(phone_number))

        if not user:
            raise ValueError("No such user")

        if not self.password_hasher.verify(str(old_pass), user.hashed_password):
            raise ValueError("Invalid password")

        if new_pass.value == old_pass.value:
            raise ValueError("Same password")

        new_password_hash = self.password_hasher.hash(str(new_pass))
        await self.user_repository.update_password(user.id, new_password_hash)

        return {
            "success" : "success",
            "message" : "Пароль успешно изменен",
            "user_id" : str(user.id)
        }