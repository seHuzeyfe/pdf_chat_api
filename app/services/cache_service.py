import json
from typing import Optional
import redis
from functools import lru_cache
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

class CacheService:
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            self.ttl = settings.CACHE_TTL
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Falling back to in-memory cache.")
            self.redis = None

    def _generate_key(self, pdf_id: str, query: str) -> str:
        """Generate a unique cache key"""
        return f"chat:{pdf_id}:{hash(query)}"

    async def get_cached_response(self, pdf_id: str, query: str) -> Optional[str]:
        """Get response from cache if it exists"""
        try:
            if self.redis:
                key = self._generate_key(pdf_id, query)
                cached = self.redis.get(key)
                if cached:
                    logger.info(f"Cache hit for query: {query[:50]}...")
                    return cached
            return None
        except Exception as e:
            logger.error(f"Cache retrieval error: {e}")
            return None

    async def cache_response(self, pdf_id: str, query: str, response: str) -> None:
        """Cache the response"""
        try:
            if self.redis:
                key = self._generate_key(pdf_id, query)
                self.redis.setex(key, self.ttl, response)
                logger.info(f"Cached response for query: {query[:50]}...")
        except Exception as e:
            logger.error(f"Cache storage error: {e}")


@lru_cache()
def get_cache_service() -> CacheService:
    return CacheService()