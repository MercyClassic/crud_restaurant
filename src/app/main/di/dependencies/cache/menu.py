from typing import Annotated

from fastapi import Depends

from app.infrastructure.cache.services.redis.menu import MenuRedisCacheService
from app.main.di.dependencies.stubs.cache import CacheInstance


def get_menu_cache_service(
    cache: Annotated[CacheInstance, Depends()],
) -> MenuRedisCacheService:
    return MenuRedisCacheService(
        cache=cache,
    )
