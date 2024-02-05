import os
from functools import partial
from typing import Any

from fastapi import FastAPI

from app.domain.interfaces.usecases.dish import DishUsecaseInterface
from app.domain.interfaces.usecases.menu import MenuUsecaseInterface
from app.domain.interfaces.usecases.submenu import SubmenuUsecaseInterface
from app.infrastructure.cache.interface import CacheServiceInterface
from app.infrastructure.database.database import (
    create_async_session_maker,
    get_async_session,
)
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.main.di.dependencies.cache import get_redis_cache_service
from app.main.di.dependencies.dish import get_dish_usecase
from app.main.di.dependencies.menu import get_menu_usecase
from app.main.di.dependencies.submenu import get_submenu_usecase
from app.main.di.dependencies.uow import get_uow
from app.main.di.stub import get_session_stub


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
    app.dependency_overrides[CacheServiceInterface] = singleton(
        get_redis_cache_service(os.environ['REDIS_HOST']),
    )
