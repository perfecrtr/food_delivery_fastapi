import redis.asyncio as redis  
from redis.asyncio.client import Redis

from app.core.config import settings

_redis_client: Redis | None = None

async def get_redis_client() -> Redis:

    global _redis_client

    if _redis_client is None:
        _redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=getattr(settings, "redis_db", 1),
            password=getattr(settings, "redis_password", None),
            decode_responses=True,
        )

    return _redis_client
    
