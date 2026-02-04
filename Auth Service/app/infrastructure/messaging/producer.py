from typing import Optional, Dict, Any, Union
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from dataclasses import asdict, is_dataclass
from datetime import datetime
from uuid import uuid4
import logging
from app.core.config import settings
import json
from app.domain.events import UserRegisteredEvent

logger = logging.getLogger(__name__)

class KafkaEventProducer:
    """Async Kafka event producer"""
    _instance: Optional['KafkaEventProducer'] = None
    _producer: Optional[AIOKafkaProducer] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
    
    async def start(self):
        if self._producer is not None:
            try:
                if not self._producer._closed:
                    logger.info("Kafka Producer is already started")
                    return
            except AttributeError:
                pass
        
        config = self._build_config()
        self._producer = AIOKafkaProducer(**config)

        try:
            await self._producer.start()
            logger.info("Kafka Producer successfully started")
        except Exception as e:
            logger.error(f"Kafka Producer starting error: {e}")
            raise

    async def stop(self):
        if self._producer is not None:
            try:
                await self._producer.stop()
                logger.info("Kafka Producer stopped")
            except Exception as e:
                logger.error(f"Kafka Producer stopping error: {e}")
            finally:
                self._producer = None

    def _build_config(self) -> Dict[str, Any]:
        config = {
            'bootstrap_servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'client_id': settings.KAFKA_CLIENT_ID,
            'acks': settings.KAFKA_PRODUCER_ACKS,
            'retries': settings.KAFKA_PRODUCER_RETRIES,
            'compression_type': settings.KAFKA_PRODUCER_COMPRESSION_TYPE
        }

        return config
    
    def _serialize_value(self, value: Any) -> bytes:
        if isinstance(value, bytes):
            return value
        elif isinstance(value, str):
            return value.encode('utf-8')
        elif is_dataclass(value):
            return json.dumps(self._dataclass_to_dict(value), default=self._json_serializer).encode('utf-8')
        elif isinstance(value, dict):
            return json.dumps(value,default=self._json_serializer).encode('utf-8')
        else:
            raise ValueError(f"Unsupported data type: {type(value)}")
        
    def _dataclass_to_dict(self, obj) -> Dict[str, Any]:
        data = asdict(obj)
        for key, value in data.items():
            if is_dataclass(value):
                data[key] = self._dataclass_to_dict(value)
        return data
    
    def _json_serializer(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _create_event_envelope(self, event_data: Any, event_type: str = None) -> Dict[str, Any]:
        envelope = {
            'event_id': str(uuid4()),
            'event_type': event_type or type(event_data).__name__,
            'timestamp': datetime.utcnow().isoformat(),
            'producer': settings.KAFKA_CLIENT_ID,
            'version': 1,
            'data': event_data
        }
        
        if is_dataclass(event_data):
            envelope['data'] = self._dataclass_to_dict(event_data)
        elif isinstance(event_data, dict):
            envelope['data'] = event_data
        
        return envelope
    
    async def send_event(
        self,
        topic: str,
        event_data: Union[Any, Dict[str, Any]],
        key: Optional[str] = None,
        event_type: Optional[str] = None,
        partition: Optional[int] = None
    ) -> bool:
        
        if self._producer is None:
            raise RuntimeError("Kafka Producer is not started")
        try:
            if self._producer._closed:
                raise RuntimeError("Kafka Producer is closed")
        except AttributeError:
            raise RuntimeError("Kafka Producer is not properly initialized")

        event_envelope = self._create_event_envelope(event_data, event_type)
        
        key_bytes = None
        if key:
            if isinstance(key, str):
                key_bytes = key.encode('utf-8')
            elif isinstance(key, bytes):
                key_bytes = key
            else:
                key_bytes = str(key).encode('utf-8')
        
        try:
            value_bytes = self._serialize_value(event_envelope)
        except Exception as e:
            logger.error(f"Ошибка сериализации события: {e}")
            return False
        
        try:
            await self._producer.send_and_wait(
                topic=topic,
                value=value_bytes,
                key=key_bytes,
                partition=partition
            )
            
            logger.debug(
                f"Event sended to topic '{topic}': "
                f"event_id={event_envelope['event_id']}, "
                f"event_type={event_envelope['event_type']}"
            )
            return True
            
        except KafkaError as e:
            logger.error(f"Event sending error (topic: {topic}): {e}")
            return False
        except Exception as e:
            logger.error(f"Error {e}")
            return False
    
    async def publish_user_registered(
        self,
        user_id: int,
        phone_number: str
    ) -> bool:
        
        event = UserRegisteredEvent(
            user_id=user_id,
            phone_number=phone_number
        )

        return await self.send_event(
            topic=settings.KAFKA_TOPIC_USER_REGISTERED,
            event_data=event,
            key=str(user_id),
            event_type = "user.registered"
        )
    
    @property
    def is_connected(self) -> bool:
        return self._producer is not None and not self._producer._closed

