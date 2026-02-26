from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
import jwt

from app.domain.repositories.courier_repository import CourierRepository
from app.domain.repositories.delivery_repository import DeliveryRepository
from app.domain.services.user_service import UserService
from app.application.commands.register_courier import RegisterCourierHandler
from app.application.commands.update_courier_status import UpdateCourierStatusHandler
from app.application.commands.update_delivery_status import UpdateDeliveryStatusHandler
from app.application.queries.get_available_couriers import GetAvailableCouriersHandler
from app.application.queries.get_delivery_by_id import GetDeliveryByIdHandler
from app.application.queries.get_current_delivery import GetCurrentDeliveryHandler
from app.infrastructure.db.database import get_db
from app.infrastructure.db.repositories.courier_repository import SQLAlchemyCourierRepository
from app.infrastructure.db.repositories.delivery_repository import SQLAlchemyDeliveryRepository
from app.infrastructure.services.user_service import  UserServiceHttpAdapter
from app.infrastructure.messaging.producer import KafkaEventProducer
from app.core.config import settings

security = HTTPBearer()

async def get_courier_repository(
    db: AsyncSession = Depends(get_db)
) -> CourierRepository:
    return SQLAlchemyCourierRepository(db)

async def get_delivery_repository(
    db: AsyncSession = Depends(get_db)
) -> DeliveryRepository:
    return SQLAlchemyDeliveryRepository(db)

async def get_user_service() -> UserService:
    return UserServiceHttpAdapter()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = int(payload["sub"])

        return user_id
    
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
    
def get_kafka_producer(request: Request) -> KafkaEventProducer:
    """
    Get kafka event producer instance (must be started via lifecycle)
    """
    producer = getattr(request.app.state, "event_producer", None)
    if producer is None:
        raise HTTPException(
            status_code=503,
            detail="Kafka producer not available"
        )
    return producer
    
async def get_courier_registration_handler(
    repo: CourierRepository = Depends(get_courier_repository),
    user_service: UserService = Depends(get_user_service)
) -> RegisterCourierHandler:
    return RegisterCourierHandler(repo=repo, user_service=user_service)

async def get_courier_status_updating_handler(
    repo: CourierRepository = Depends(get_courier_repository),
) ->  UpdateCourierStatusHandler:
    return UpdateCourierStatusHandler(repo=repo)

async def get_available_couriers_getting_handler(
    repo: CourierRepository = Depends(get_courier_repository)
) -> GetAvailableCouriersHandler:
    return GetAvailableCouriersHandler(repo=repo)

async def get_delivery_getting_by_id_handler(
    repo: DeliveryRepository = Depends(get_delivery_repository)
) -> GetDeliveryByIdHandler:
    return GetDeliveryByIdHandler(repo=repo)

async def get_delivery_status_updating_handler(
    courier_repo: CourierRepository = Depends(get_courier_repository),
    delivery_repo: DeliveryRepository = Depends(get_delivery_repository),
    producer: KafkaEventProducer = Depends(get_kafka_producer)
) -> UpdateDeliveryStatusHandler:
    return UpdateDeliveryStatusHandler(courier_repo=courier_repo, delivery_repo=delivery_repo, producer=producer)

async def get_current_delivery_getting_handler(
    courier_repo: CourierRepository = Depends(get_courier_repository),
    delivery_repo: DeliveryRepository = Depends(get_delivery_repository),
) -> GetCurrentDeliveryHandler:
    return GetCurrentDeliveryHandler(courier_repo=courier_repo, delivery_repo=delivery_repo)

