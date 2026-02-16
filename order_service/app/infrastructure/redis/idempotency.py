from typing import Callable, Awaitable, TypeVar
from fastapi import HTTPException, status
import json

from app.domain.services.idempotency_service import IdempotencyService
from app.infrastructure.redis.client import get_redis_client
from app.core.config import settings

T = TypeVar("T")

class RedisIdempotencyService(IdempotencyService):

    async def run(
        self,
        key: str,
        fingerprint: str,
        action: Callable[[], Awaitable[T]],
    ) -> T:
        redis = await get_redis_client()
        redis_key = f"idempotency:{key}"

        raw = await redis.get(redis_key)
        if raw:
            data = json.loads(raw)
            if data["fingerprint"] != fingerprint:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Idempotency key already used for a different request",
                )
            return data["result"]

        result = await action()

        await redis.setex(
            redis_key,
            settings.redis_ttl,
            json.dumps(
                {
                    "fingerprint": fingerprint,
                    "result": result, 
                },
                default=str,
            ),
        )

        return result