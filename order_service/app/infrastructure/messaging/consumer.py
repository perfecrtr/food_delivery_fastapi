import asyncio
import json
from typing import Any, Optional, Sequence, Dict, Any
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.application.handlers.payment_events import PaymentEventsHandler
from app.application.handlers.delivery_events import DeliveryEventsHandler
from app.domain.events import PaymentProcessedEvent, DeliveryStartedEvent, DeliveryCompletedEvent
from app.domain.enums import PaymentMethodType
from app.domain.services.event_consumer import EventConsumer

class KafkaEventConsumer(EventConsumer):
    def __init__(
        self,
        *,
        payment_events_handler: PaymentEventsHandler,
        delivery_events_handler: DeliveryEventsHandler,
        group_id: str = "order-service-consumer",
        auto_offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self._payment_events_handler = payment_events_handler
        self._delivery_events_handler = delivery_events_handler

        self._consumer = AIOKafkaConsumer(
            "payment.processed",
            "delivery.started",
            "delivery.completed",
            loop=self._loop,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            client_id=settings.KAFKA_CLIENT_ID,
            group_id=group_id,
            enable_auto_commit=enable_auto_commit,
            auto_offset_reset=auto_offset_reset,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

        self._task: Optional[asyncio.Task] = None
        self._stopped = asyncio.Event()

    async def start(self) -> None:
        await self._consumer.start()
        self._stopped.clear()
        self._task = self._loop.create_task(self._consume_loop())

    async def _consume_loop(self) -> None:
        try:
            async for msg in self._consumer:
                try:
                    await self._handle_message(msg.topic, msg.value, msg)
                except Exception:
                    pass
        except asyncio.CancelledError:
            pass
        except Exception:
            pass
        finally:
            self._stopped.set()

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        await self._consumer.stop()

    async def run_forever(self) -> None:
        await self.start()
        try:
            await self._stopped.wait()
        finally:
            await self.stop()

    async def _handle_message(self, topic: str, payload: Dict[str, Any], raw_message: Any) -> None:
        if topic == "payment.processed":
            await self.handle_payment_processed(payload=payload)
        elif topic == "delivery.started":
            await self.handle_delivery_started(payload=payload)
        elif topic == "delivery.completed":
            await self.handle_delivery_completed(payload=payload)
        else:
            pass

    async def handle_payment_processed(self, payload):
        event = PaymentProcessedEvent(
            payment_id=UUID(payload["payment_id"]),
            order_id=UUID(payload["order_id"]),
            user_id=int(payload["user_id"]),
            amount=Decimal(payload["amount"]),
            result=str(payload["result"]),
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
        )

        await self._payment_events_handler.handle_payment_processed(event=event)

    async def handle_delivery_started(self, payload):
        event = DeliveryStartedEvent(
            order_id=UUID(payload["order_id"]),
            occurred_at=datetime.fromisoformat(payload["occurred_at"])
        )

        await self._delivery_events_handler.handle_delivery_started(event=event)

    async def handle_delivery_completed(self, payload):
        event = DeliveryCompletedEvent(
            order_id=UUID(payload["order_id"]),
            occurred_at=datetime.fromisoformat(payload["occurred_at"])
        )

        await self._delivery_events_handler.handle_delivery_completed(event=event)

        

    