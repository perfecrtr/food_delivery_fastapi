from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID
from typing import Optional

from app.domain.enums import PaymentMethodType

@dataclass(frozen=True)
class PaymentGatewayRequest:
    amount: float
    payment_method: PaymentMethodType
    order_id: UUID
    user_id: int
    idempotency_key: UUID

@dataclass(frozen=True)
class PaymentGatewayResponse:
    success: bool
    transaction_id: Optional[str] 
    status: str
    error_message: Optional[str] = None

class PaymentGateway(ABC):

    @abstractmethod
    async def charge(self, request: PaymentGatewayRequest) -> PaymentGatewayResponse:
        pass

    @abstractmethod
    async def get_transaction_status(self, transaction_id: str) -> str:
        pass

    @abstractmethod
    async def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        pass