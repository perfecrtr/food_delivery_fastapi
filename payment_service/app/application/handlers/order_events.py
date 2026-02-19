from uuid import uuid4
from datetime import datetime

from app.domain.repositories.payment_repository import PaymentRepository
from app.domain.services.payment_gateway import PaymentGateway, PaymentGatewayRequest, PaymentGatewayResponse
from app.domain.services.event_producer import EventProducer
from app.domain.events import OrderCreatedEvent, PaymentProcessedEvent
from app.domain.entities.payment import Payment
from app.domain.value_objects.money import Money
from app.domain.enums import PaymentMethodType, PaymentStatus

class OrderEventsHandler:
    
    def __init__(
        self,
        repo: PaymentRepository,
        gateway: PaymentGateway,
        event_producer: EventProducer
    ) -> None:
        
        self.repo = repo
        self.gateway = gateway
        self.event_producer = event_producer

    async def handle_order_created(self, event: OrderCreatedEvent) -> Payment:
        payment = Payment(
            id=uuid4(),
            order_id=event.order_id,
            user_id=event.user_id,
            restaurant_id=event.restaurant_id,
            amount=Money(event.total_price),
            status=PaymentStatus.PENDING,
            payment_method=event.payment_method,
            created_at=datetime.utcnow(),
            updated_at=None,
        )

        payment = await self.repo.create(payment)

        gateway_request = PaymentGatewayRequest(
            amount=payment.amount.amount,
            payment_method=payment.payment_method,
            order_id=payment.order_id,
            user_id=payment.user_id,
            idempotency_key=payment.id,
        )

        payment = await self.repo.update_status(payment_id=payment.id, status=PaymentStatus.PROCESSING)

        gateway_response: PaymentGatewayResponse = await self.gateway.charge(gateway_request)

        new_status = (
            PaymentStatus.COMPLETED if gateway_response.success else PaymentStatus.FAILED
        )
        payment = await self.repo.update_status(payment_id=payment.id, status=new_status)

        event = PaymentProcessedEvent(
            payment_id=payment.id,
            order_id=payment.order_id,
            user_id=payment.user_id,
            amount=payment.amount.amount,
            result=payment.status,
            occurred_at=payment.updated_at
        )

        await self.event_producer.publish(topic="payment.processed", event=event)

        return payment 
