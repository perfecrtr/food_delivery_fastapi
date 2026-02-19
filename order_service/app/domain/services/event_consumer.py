from abc import ABC, abstractmethod
from typing import Dict, Any

class EventConsumer(ABC):

    @abstractmethod
    async def handle_payment_processed(self, payload: Dict[str, Any]) -> None:
        pass