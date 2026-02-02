from dataclasses import dataclass
from typing import Optional

from redis.asyncio.client import Redis


@dataclass
class RateLimitConfig:
    max_requests: int = 5         
    window_seconds: int = 60     


class RateLimiter:
    """
    Simpler Redis Rate Limiter
    """

    def __init__(self, redis: Redis, config: Optional[RateLimitConfig] = None):
        self.redis = redis
        self.config = config or RateLimitConfig()

    async def is_allowed(self, scope: str, identity: str) -> bool:
        key = f"rl:{scope}:{identity}"
        current = await self.redis.incr(key)

        if current == 1:
            await self.redis.expire(key, self.config.window_seconds)

        return current <= self.config.max_requests

    async def get_remaining(self, scope: str, identity: str) -> int:
        key = f"rl:{scope}:{identity}"
        value = await self.redis.get(key)
        if value is None:
            return self.config.max_requests
        try:
            used = int(value)
        except ValueError:
            return 0
        remaining = self.config.max_requests - used
        return remaining if remaining > 0 else 0