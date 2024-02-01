from typing import Annotated

from fastapi import Depends

from app.domain.usecases.dish import DishUsecase
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


def get_dish_usecase(
    uow: Annotated[UoWInterface, Depends()],
) -> DishUsecase:
    return DishUsecase(
        uow=uow,
    )
