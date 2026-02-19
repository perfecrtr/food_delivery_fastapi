from uuid import uuid4
from typing import Optional
from asyncio import sleep, TimeoutError
from datetime import datetime
import random
import hashlib
import hmac

from app.domain.services.payment_gateway import PaymentGateway, PaymentGatewayRequest, PaymentGatewayResponse
from app.domain.enums import PaymentMethodType

class MockPaymentGatewayAdapter():

    def __init__(
        self,
        success_rate: float = 0.5,
        min_delay: float = 0.5,
        max_delay: float = 10.0,
        webhook_secret: Optional[str] = None
    ):
        self.success_rate = success_rate
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.webhook_secret = webhook_secret or "default_secret"

        self.transactions = {}

    async def charge(self, request: PaymentGatewayRequest) -> PaymentGatewayResponse:
        try:

            delay = random.uniform(self.min_delay, self.max_delay)
            await sleep(delay=delay)

            scenario = await self._determinate_scenario()

            if scenario == "success":
                return await self._handle_success(request)
            elif scenario == "insufficient_funds":
                return await self._handle_insufficient_funds(request)
            elif scenario == "declined":
                return await self._handle_declined(request)
            else:
                return await self._handle_success(request)
            
        except TimeoutError:
            raise ValueError("Payment gateway timeout")
        except Exception as e:
            raise ValueError(f"Gateway error: {str(e)}")


    async def get_transaction_status(self, transaction_id: str) -> str:
        if transaction_id in self.transactions:
            return self.transactions[transaction_id]["status"]
        return "not_found"
    
    async def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        expected = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected, signature)

    async def _determinate_scenario(self) -> str:
        if random.random() < self.success_rate:
            return "success"
        else:
            return random.choice(["insufficient_funds", "declined"])
        
    async def _handle_success(self, request: PaymentGatewayRequest) -> PaymentGatewayResponse:
        transaction_id = f"txn_{uuid4().hex[:16]}"
        self.transactions[transaction_id] = {
            "request": {
                "amount": request.amount,
                "order_id": str(request.order_id)
            },
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }

        return PaymentGatewayResponse(
            success=True,
            transaction_id=transaction_id,
            status="completed",
            error_message=None
        )

    async def _handle_insufficient_funds(self, request: PaymentGatewayRequest) -> PaymentGatewayResponse:

        return PaymentGatewayResponse(
            success=False,
            transaction_id=None,
            status="failed",
            error_message="Insufficient funds"
        )
    
    async def _handle_declined(self, request: PaymentGatewayRequest) -> PaymentGatewayResponse:

        return PaymentGatewayResponse(
            success=False,
            transaction_id=None,
            status="failed",
            error_message="Was declined by issuer"
        )