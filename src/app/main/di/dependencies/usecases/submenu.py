from typing import Annotated

from fastapi import Depends

from app.domain.usecases.submenu import SubmenuUsecase
from app.infrastructure.cache.interfaces.submenu import SubmenuCacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


def get_submenu_usecase(
    uow: Annotated[UoWInterface, Depends()],
    cache: Annotated[SubmenuCacheServiceInterface, Depends()],
) -> SubmenuUsecase:
    return SubmenuUsecase(
        uow=uow,
        cache=cache,
    )
