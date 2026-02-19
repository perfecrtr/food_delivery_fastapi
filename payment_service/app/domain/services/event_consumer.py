from abc import ABC, abstractmethod
from typing import Dict, Any

class EventConsumer(ABC):

    @abstractmethod
    async def handle_order_created(self, payload: Dict[str, Any]) -> None:
        pass