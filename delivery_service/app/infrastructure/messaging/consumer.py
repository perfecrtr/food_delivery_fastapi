import asyncio
import json
from typing import Any, Optional, Sequence, Dict, Any
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from aiokafka import AIOKafkaConsumer

from app.core.config import settings
from app.application.handlers.order_events import OrderEventsHandler
from app.domain.services.event_consumer import EventConsumer
from app.domain.events import OrderPaidEvent, OrderCancelledEvent

class KafkaEventConsumer(EventConsumer):
    def __init__(
        self,
        *,
        order_events_handler: OrderEventsHandler,
        group_id: str = "delivery-service-consumer",
        auto_offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self._order_events_handler = order_events_handler

        self._consumer = AIOKafkaConsumer(
            "order.paid",
            "order.cancelled",
            loop=self._loop,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            client_id=settings.kafka_client_id,
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
        if topic == "order.paid":
            await self.handle_order_paid(payload=payload)
        elif topic == "order.cancelled":
            await self.handle_order_cancelled(payload=payload)
        else:
            pass

    async def handle_order_paid(self, payload):
        event = OrderPaidEvent(
            order_id=UUID(payload["order_id"]),
            delivery_address=dict(payload["delivery_address"]),
            restaurant_address=dict(payload["restaurant_address"]),
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
        )

        await self._order_events_handler.handle_order_paid(event=event)

    async def handle_order_cancelled(self, payload):
        event = OrderCancelledEvent(
            order_id=UUID(payload["order_id"]),
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
        )

        await self._order_events_handler.handle_order_cancelled(event=event)
        

    