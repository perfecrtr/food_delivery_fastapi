import json
import asyncio
import logging
from typing import Optional, Dict, Callable, Awaitable
from aiokafka import AIOKafkaConsumer
from app.core.config import settings

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self):
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.handlers: Dict[str, Callable] = {}
        self.is_running = False
    
    async def connect(self):
        """Connect to Kafka with logging"""
        try:
            logger.info(f"Connecting to Kafka: {settings.KAFKA_BOOTSTRAP_SERVERS}")
            logger.info(f"Topic: {settings.KAFKA_TOPIC_USER_REGISTERED}")
            logger.info(f"Group: {settings.KAFKA_CONSUMER_GROUP}")
            
            self.consumer = AIOKafkaConsumer(
                settings.KAFKA_TOPIC_USER_REGISTERED,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                group_id=settings.KAFKA_CONSUMER_GROUP,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
                max_poll_records=10,
                session_timeout_ms=30000,
                heartbeat_interval_ms=3000
            )
            
            await self.consumer.start()
            logger.info("Kafka consumer connected and started")
            
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise
    
    def register_handler(self, topic: str, handler: Callable[[Dict], Awaitable[None]]):
        """Register handler for topic"""
        self.handlers[topic] = handler
        logger.info(f"Registered handler for topic: {topic}")
    
    async def consume(self):
        """Start consuming messages"""
        if not self.consumer:
            await self.connect()
        
        self.is_running = True
        logger.info(f"Starting to consume from {settings.KAFKA_TOPIC_USER_REGISTERED}")
        
        try:
            async for message in self.consumer:
                if not self.is_running:
                    break
                    
                await self._process_message(message)
                
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled")
        except Exception as e:
            logger.error(f"Consumer error: {e}", exc_info=True)
        finally:
            await self.close()
    
    async def _process_message(self, message):
        """Process single Kafka message"""
        topic = message.topic
        value = message.value
        
        logger.info(f"Received message from {topic}")
        logger.debug(f"Message: {value}")
        
        if topic in self.handlers:
            try:
                logger.info(f"Processing message from {topic}")
                await self.handlers[topic](value)
                logger.info(f"Successfully processed message from {topic}")
            except Exception as e:
                logger.error(f"Handler error for topic {topic}: {e}", exc_info=True)
        else:
            logger.warning(f" No handler registered for topic: {topic}")
    
    async def close(self):
        """Close consumer connection"""
        self.is_running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")


kafka_consumer = KafkaConsumer()