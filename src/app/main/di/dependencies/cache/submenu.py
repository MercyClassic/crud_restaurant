from typing import Annotated

from fastapi import Depends

from app.infrastructure.cache.services.redis.submenu import SubmenuRedisCacheService
from app.main.di.dependencies.stubs.cache import CacheInstance


def get_submenu_cache_service(
    cache: Annotated[CacheInstance, Depends()],
) -> SubmenuRedisCacheService:
    return SubmenuRedisCacheService(
        cache=cache,
    )
