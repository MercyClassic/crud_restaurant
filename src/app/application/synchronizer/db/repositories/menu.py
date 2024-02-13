from typing import Iterable
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.synchronizer.models import Menu
from app.infrastructure.database.models import Menu as MenuDB


class MenuRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def _convert_menus(self, menus: Iterable[Menu]):
        return [
            {
                'id': menu.id,
                'title': menu.title,
                'description': menu.description,
            }
            for menu in menus
        ]

    async def get_menus(self) -> Iterable[MenuDB]:
        result = await self._session.execute(select(MenuDB))
        return result.scalars().all()

    async def bulk_delete_menus(self, menus: Iterable[UUID]) -> None:
        stmt = delete(MenuDB).where(MenuDB.id.in_(menus))
        await self._session.execute(stmt)

    async def update_menu(self, menu: Menu) -> None:
        stmt = (
            update(MenuDB)
            .values(
                title=menu.title,
                description=menu.description,
            )
            .where(MenuDB.id == menu.id)
        )
        await self._session.execute(stmt)

    async def bulk_insert_menus(self, menus: Iterable[Menu]) -> None:
        data_to_insert = self._convert_menus(menus)
        stmt = insert(MenuDB).values(
            data_to_insert,
        )
        await self._session.execute(stmt)
