from typing import Annotated

from fastapi import Depends

from app.infrastructure.cache.services.redis.dish import DishRedisCacheService
from app.main.di.dependencies.stubs.cache import CacheInstance


def get_dish_cache_service(
    cache: Annotated[CacheInstance, Depends()],
) -> DishRedisCacheService:
    return DishRedisCacheService(
        cache=cache,
    )
