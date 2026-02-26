from abc import ABC, abstractmethod
from typing import Protocol

class DomainEvent(Protocol):
    pass

class EventProducer(ABC):

    @abstractmethod
    async def publish(self, topic: str, event: DomainEvent) -> None:
        pass