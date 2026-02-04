"""
Dependency injection for FastAPI
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio.client import Redis

from app.domain.services.password_hasher import PasswordHasher
from app.domain.services.token_service import TokenService
from app.infrastructure.db.database import get_db
from app.infrastructure.db.repository import UserRepository
from app.infrastructure.db.models import UserModel
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_service import JWTService
from app.application.commands.register_user import RegisterUserHandler
from app.application.commands.login_user import UserLoginHandler
from app.application.commands.change_password import UserChangePasswordHandler
from app.infrastructure.redis.client import get_redis_client
from app.infrastructure.redis.rate_limiter import RateLimiter, RateLimitConfig
from app.infrastructure.redis.token_store import TokenStore, TokenStoreConfig
from app.infrastructure.messaging.producer import KafkaEventProducer, kafka_event_producer
from app.core.config import settings

security = HTTPBearer()


def get_password_hasher() -> PasswordHasher:
    """
    Get password hasher instance
    """
    return BcryptPasswordHasher()


def get_token_service() -> TokenService:
    """
    Get token service instance
    """
    return JWTService()


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """
    Get user repository instance
    """
    return UserRepository(db)

def get_kafka_producer() -> KafkaEventProducer:
    """
    Get kafka event producer instance (must be started via lifecycle)
    """
    if kafka_event_producer is None:
        raise RuntimeError("Kafka producer is not initialized. Ensure app startup completed.")
    return kafka_event_producer

async def get_register_handler(user_repository = Depends(get_user_repository),
                         password_hasher = Depends(get_password_hasher),
                         token_service = Depends(get_token_service),
                         kafka_producer: KafkaEventProducer = Depends(get_kafka_producer)):
    return(
        RegisterUserHandler(
        user_repository,
        password_hasher,
        token_service,
        kafka_producer
        )
    )

async def get_login_handler(user_repository = Depends(get_user_repository),
                         password_hasher = Depends(get_password_hasher),
                         token_service = Depends(get_token_service)):
    return(
        UserLoginHandler(
        user_repository,
        password_hasher,
        token_service
        )
    )

async def get_change_password_handler(user_repository = Depends(get_user_repository),
                         password_hasher = Depends(get_password_hasher)):
    return(
        UserChangePasswordHandler(
        user_repository,
        password_hasher
        )
    )

def get_redis() -> Redis:
    return get_redis_client()


def get_login_rate_limiter(
    redis: Redis = Depends(get_redis),
) -> RateLimiter:
    config = RateLimitConfig(
        max_requests=5,
        window_seconds=60,
    )
    return RateLimiter(redis, config)

def get_token_store(
    redis: Redis = Depends(get_redis),
) -> TokenStore:
    refresh_ttl = settings.refresh_token_expire_days * 24 * 60 * 60
    access_ttl = settings.access_token_expire_minutes * 60
    config = TokenStoreConfig(
        refresh_ttl=refresh_ttl,
        access_ttl=access_ttl,
    )
    return TokenStore(redis, config)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Depends(get_token_service),
    token_store: TokenStore = Depends(get_token_store)
    ) -> int:
    """
    Get current user ID from JWT token
    """
    token = credentials.credentials
    
    try:
        payload = token_service.verify_access_token(token)
        user_id = payload.get('user_id')
        jti = payload.get('jti')
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        if jti and await token_store.is_access_token_blacklisted(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            )
        
        return user_id
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserModel:
    """
    Get current user from database
    """
    user = await user_repository.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


async def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    token_service: TokenService = Depends(get_token_service)
) -> Optional[int]:
    """
    Get current user ID from JWT token (optional)
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    
    try:
        payload = token_service.verify_access_token(token)
        user_id = payload.get('user_id')
        return user_id if user_id else None
    except (ValueError, HTTPException):
        return None


async def get_optional_user(
    user_id: Optional[int] = Depends(get_optional_user_id),
    user_repository: UserRepository = Depends(get_user_repository)
) -> Optional[UserModel]:
    """
    Get current user from database (optional)
    """
    if not user_id:
        return None
    
    return await user_repository.get_by_id(user_id)

