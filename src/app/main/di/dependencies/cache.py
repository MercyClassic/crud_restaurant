from redis import Redis

from app.infrastructure.cache.redis.service import RedisCacheService


def get_redis_cache_service(host: str) -> RedisCacheService:
    redis = Redis(host, decode_responses=True)
    return RedisCacheService(redis)
