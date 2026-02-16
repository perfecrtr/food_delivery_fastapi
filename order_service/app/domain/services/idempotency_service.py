from typing import Callable, Awaitable, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T") 

class IdempotencyService(ABC):

    @abstractmethod
    async def run(
        self,
        key: str,
        fingerprint: str,
        action: Callable[[], Awaitable[T]],
    ) -> T:
        pass