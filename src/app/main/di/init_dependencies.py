import os
from functools import partial
from typing import Any

from fastapi import FastAPI

from app.domain.interfaces.usecases.dish import DishUsecaseInterface
from app.domain.interfaces.usecases.menu import MenuUsecaseInterface
from app.domain.interfaces.usecases.submenu import SubmenuUsecaseInterface
from app.infrastructure.cache.interfaces.dish import DishCacheServiceInterface
from app.infrastructure.cache.interfaces.menu import MenuCacheServiceInterface
from app.infrastructure.cache.interfaces.submenu import SubmenuCacheServiceInterface
from app.infrastructure.database.database import (
    create_async_session_maker,
    get_async_session,
)
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.main.di.dependencies.cache.dish import get_dish_cache_service
from app.main.di.dependencies.cache.instance import get_redis_instance
from app.main.di.dependencies.cache.menu import get_menu_cache_service
from app.main.di.dependencies.cache.submenu import get_submenu_cache_service
from app.main.di.dependencies.stubs.cache import CacheInstance
from app.main.di.dependencies.stubs.session import get_session_stub
from app.main.di.dependencies.uow import get_uow
from app.main.di.dependencies.usecases.dish import get_dish_usecase
from app.main.di.dependencies.usecases.menu import get_menu_usecase
from app.main.di.dependencies.usecases.submenu import get_submenu_usecase


def singleton(instance: Any) -> Any:
    def wrapper() -> Any:
        return instance

    return wrapper


def init_dependencies(app: FastAPI) -> None:
    async_session_maker = create_async_session_maker(os.environ['db_uri'])

    app.dependency_overrides[get_session_stub] = partial(
        get_async_session,
        async_session_maker,
    )
    app.dependency_overrides[UoWInterface] = get_uow
    app.dependency_overrides[DishUsecaseInterface] = get_dish_usecase
    app.dependency_overrides[MenuUsecaseInterface] = get_menu_usecase
    app.dependency_overrides[SubmenuUsecaseInterface] = get_submenu_usecase
    app.dependency_overrides[CacheInstance] = singleton(
        get_redis_instance(os.environ['REDIS_HOST']),
    )
    app.dependency_overrides[DishCacheServiceInterface] = get_dish_cache_service
    app.dependency_overrides[MenuCacheServiceInterface] = get_menu_cache_service
    app.dependency_overrides[SubmenuCacheServiceInterface] = get_submenu_cache_service
