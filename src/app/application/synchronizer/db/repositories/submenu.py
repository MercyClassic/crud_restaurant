from typing import Iterable
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.synchronizer.models import Submenu
from app.infrastructure.database.models import Submenu as SubmenuDB


class SubmenuRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def _convert_submenus(self, submenus: Iterable[Submenu]):
        return [
            {
                'id': submenu.id,
                'title': submenu.title,
                'description': submenu.description,
                'menu_id': submenu.menu_id,
            }
            for submenu in submenus
        ]

    async def get_submenus(self) -> Iterable[SubmenuDB]:
        result = await self._session.execute(select(SubmenuDB))
        return result.scalars().all()

    async def bulk_delete_submenus(self, submenus: Iterable[UUID]) -> None:
        stmt = delete(SubmenuDB).where(SubmenuDB.id.in_(submenus))
        await self._session.execute(stmt)

    async def update_submenu(self, submenu: Submenu) -> None:
        stmt = (
            update(SubmenuDB)
            .values(
                title=submenu.title,
                description=submenu.description,
                submenu_id=submenu.menu_id,
            )
            .where(SubmenuDB.id == submenu.id)
        )
        await self._session.execute(stmt)

    async def bulk_insert_submenus(self, submenus: Iterable[Submenu]) -> None:
        data_to_insert = self._convert_submenus(submenus)
        stmt = insert(SubmenuDB).values(
            data_to_insert,
        )
        await self._session.execute(stmt)
