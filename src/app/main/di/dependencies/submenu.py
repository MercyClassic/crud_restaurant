from typing import Annotated

from fastapi import Depends

from app.domain.usecases.submenu import SubmenuUsecase
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


def get_submenu_usecase(
    uow: Annotated[UoWInterface, Depends()],
):
    return SubmenuUsecase(
        uow=uow,
    )
