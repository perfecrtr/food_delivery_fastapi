from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Dict, Any

from redis.asyncio.client import Redis


@dataclass
class TokenStoreConfig:
    refresh_ttl: int  
    access_ttl: int 


class TokenStore:
    def __init__(self, redis: Redis, config: TokenStoreConfig):
        self.redis = redis
        self.config = config

    async def save_refresh_session(self, sid: str, user_id: int) -> None:
        key = f"rt:sess:{sid}"
        await self.redis.set(key, str(user_id), ex=self.config.refresh_ttl)

    async def get_refresh_session(self, sid: str) -> Optional[int]:
        key = f"rt:sess:{sid}"
        value = await self.redis.get(key)
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    async def delete_refresh_session(self, sid: str) -> None:
        key = f"rt:sess:{sid}"
        await self.redis.delete(key)

    async def rotate_refresh_session(
        self,
        old_sid: str,
        new_sid: str,
        user_id: int,
    ) -> None:
        await self.delete_refresh_session(old_sid)
        await self.save_refresh_session(new_sid, user_id)

    async def blacklist_access_token(self, jti: str, ttl_seconds: Optional[int] = None) -> None:
        key = f"at:blacklist:{jti}"
        ttl = ttl_seconds or self.config.access_ttl
        await self.redis.set(key, "1", ex=ttl)

    async def is_access_token_blacklisted(self, jti: str) -> bool:
        key = f"at:blacklist:{jti}s"
        return await self.redis.exists(key) == 1