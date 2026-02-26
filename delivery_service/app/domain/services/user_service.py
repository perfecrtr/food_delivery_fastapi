from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class UserServiceResponse:
    name: str
    phone: str

class UserService(ABC):

    @abstractmethod
    async def get_user_info(
        self, 
        user_id: int,
    ) -> UserServiceResponse:
        pass