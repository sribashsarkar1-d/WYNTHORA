import json
import logging
from typing import Any, Optional
import aioredis
from app.core.config import settings

logger = logging.getLogger("RedisCache")

class RedisCache:
    """
    Enterprise Distributed Caching Layer.
    """
    def __init__(self):
        self.redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        try:
            self.redis = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
            logger.info("Connected to Redis cache.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")

    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            return None
        try:
            val = await self.redis.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.warning(f"Redis get failed for {key}: {e}")
        return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 60):
        if not self.redis:
            return
        try:
            await self.redis.set(key, json.dumps(value), ex=ttl_seconds)
        except Exception as e:
            logger.warning(f"Redis set failed for {key}: {e}")

redis_cache = RedisCache()
