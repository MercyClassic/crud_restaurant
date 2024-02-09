from typing import Annotated

from fastapi import Depends

from app.domain.usecases.menu import MenuUsecase
from app.infrastructure.cache.interfaces.menu import MenuCacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


def get_menu_usecase(
    uow: Annotated[UoWInterface, Depends()],
    cache: Annotated[MenuCacheServiceInterface, Depends()],
) -> MenuUsecase:
    return MenuUsecase(
        uow=uow,
        cache=cache,
    )
