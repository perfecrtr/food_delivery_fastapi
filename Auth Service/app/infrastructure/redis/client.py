from functools import lru_cache

import redis.asyncio as redis  
from redis.asyncio.client import Redis

from app.core.config import settings


@lru_cache
def get_redis_client() -> Redis:
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=getattr(settings, "redis_db", 0),
        password=getattr(settings, "redis_password", None),
        decode_responses=True, 
    )