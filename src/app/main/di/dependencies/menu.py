from typing import Annotated

from fastapi import Depends

from app.domain.usecases.menu import MenuUsecase
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


def get_menu_usecase(
    uow: Annotated[UoWInterface, Depends()],
) -> MenuUsecase:
    return MenuUsecase(
        uow=uow,
    )
