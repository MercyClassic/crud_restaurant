from typing import Annotated

from fastapi import Depends

from app.domain.services.menu import MenuService
from app.infrastructure.cache.interfaces.menu import MenuCacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


def get_menu_usecase(
    uow: Annotated[UoWInterface, Depends()],
    cache: Annotated[MenuCacheServiceInterface, Depends()],
) -> MenuService:
    return MenuService(
        uow=uow,
        cache=cache,
    )
