from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from app.domain.entities.payment import Payment
from app.domain.enums import PaymentStatus

class PaymentRepository(ABC):

    @abstractmethod
    async def create(self, payment_data: Payment) -> Payment:
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> Optional[Payment]:
        pass

    @abstractmethod
    async def update_status(self, payment_id: UUID, status: PaymentStatus, transaction_id: Optional[str]) -> Optional[Payment]:
        pass