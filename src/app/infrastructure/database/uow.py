from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.repositories.dish import DishRepository
from app.infrastructure.database.repositories.menu import MenuRepository
from app.infrastructure.database.repositories.submenu import SubmenuRepository


class UoW:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.dish_repo = DishRepository(self._session)
        self.menu_repo = MenuRepository(self._session)
        self.submenu_repo = SubmenuRepository(self._session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
