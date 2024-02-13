from sqlalchemy.ext.asyncio import AsyncSession

from app.application.synchronizer.db.repositories.dish import DishRepository
from app.application.synchronizer.db.repositories.menu import MenuRepository
from app.application.synchronizer.db.repositories.submenu import SubmenuRepository


class SynchronizerUow:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.menu_repo = MenuRepository(self._session)
        self.submenu_repo = SubmenuRepository(self._session)
        self.dish_repo = DishRepository(self._session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
