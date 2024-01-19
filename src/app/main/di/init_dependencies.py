import os
from functools import partial

from fastapi import FastAPI

from app.domain.interfaces.usecases.dish import DishUsecaseInterface
from app.domain.interfaces.usecases.menu import MenuUsecaseInterface
from app.domain.interfaces.usecases.submenu import SubmenuUsecaseInterface
from app.infrastructure.database.database import (
    create_async_session_maker,
    get_async_session,
)
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.main.di.dependencies.dish import get_dish_usecase
from app.main.di.dependencies.menu import get_menu_usecase
from app.main.di.dependencies.submenu import get_submenu_usecase
from app.main.di.dependencies.uow import get_uow
from app.main.di.stub import get_session_stub


def init_dependencies(app: FastAPI):
    async_session_maker = create_async_session_maker(os.environ['db_uri'])

    app.dependency_overrides[get_session_stub] = partial(
        get_async_session,
        async_session_maker,
    )
    app.dependency_overrides[UoWInterface] = get_uow
    app.dependency_overrides[DishUsecaseInterface] = get_dish_usecase
    app.dependency_overrides[MenuUsecaseInterface] = get_menu_usecase
    app.dependency_overrides[SubmenuUsecaseInterface] = get_submenu_usecase