from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
import jwt

from app.infrastructure.db.database import get_db
from app.infrastructure.db.repositories.order_repository import SQLAlchemyOrderRepository
from app.infrastructure.services.restaurant_service import RestaurantServiceHttpAdapter
from app.application.commands.create_order import CreateOrderHandler
from app.application.commands.cancel_order import CancelOrderHandler
from app.application.queries.get_orders import GetOrdersHandler
from app.core.config import settings

security = HTTPBearer()

async def get_order_repository(
    db: AsyncSession = Depends(get_db),
) -> SQLAlchemyOrderRepository:
    return SQLAlchemyOrderRepository(db)

async def get_restaurant_service() -> RestaurantServiceHttpAdapter:
    return RestaurantServiceHttpAdapter()

async def get_order_creating_handler(
    repo: SQLAlchemyOrderRepository = Depends(get_order_repository),
    restaurant_service: RestaurantServiceHttpAdapter = Depends(get_restaurant_service)
) -> CreateOrderHandler:
    return CreateOrderHandler(repo=repo, restaurant_service=restaurant_service)

async def get_order_getting_handler(
    repo: SQLAlchemyOrderRepository = Depends(get_order_repository)
) -> GetOrdersHandler:
    return GetOrdersHandler(repo=repo)

async def get_order_cancelling_handler(
    repo: SQLAlchemyOrderRepository = Depends(get_order_repository)
) -> CancelOrderHandler:
    return CancelOrderHandler(repo=repo)

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