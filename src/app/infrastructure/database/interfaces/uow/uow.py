from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.interfaces.repositories.dish import (
    DishRepositoryInterface,
)
from app.infrastructure.database.interfaces.repositories.menu import (
    MenuRepositoryInterface,
)
from app.infrastructure.database.interfaces.repositories.submenu import (
    SubRepositoryInterface,
)


class UoWInterface:
    _session: AsyncSession
    dish_repo: DishRepositoryInterface
    menu_repo: MenuRepositoryInterface
    submenu_repo: SubRepositoryInterface

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError
