from typing import Iterable

from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.synchronizer.models import Dish, Menu, Submenu
from app.infrastructure.database.models import Dish as DishDB
from app.infrastructure.database.models import Menu as MenuDB
from app.infrastructure.database.models import Submenu as SubmenuDB


class SyncRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def clear_db(self) -> None:
        stmt = delete(MenuDB)
        await self._session.execute(stmt)

    async def bulk_insert_menus(self, menus: Iterable[Menu]) -> None:
        data_to_insert = [
            {
                'id': menu.id,
                'title': menu.title,
                'description': menu.description,
            }
            for menu in menus
        ]
        stmt = insert(MenuDB).values(
            data_to_insert,
        )
        await self._session.execute(stmt)

    async def bulk_insert_submenus(self, submenus: Iterable[Submenu]) -> None:
        data_to_insert = [
            {
                'id': submenu.id,
                'title': submenu.title,
                'description': submenu.description,
                'menu_id': submenu.menu_id,
            }
            for submenu in submenus
        ]
        stmt = insert(SubmenuDB).values(
            data_to_insert,
        )
        await self._session.execute(stmt)

    async def bulk_insert_dishes(self, dishes: Iterable[Dish]) -> None:
        data_to_insert = [
            {
                'id': dish.id,
                'title': dish.title,
                'description': dish.description,
                'price': dish.price,
                'submenu_id': dish.submenu_id,
            }
            for dish in dishes
        ]
        stmt = insert(DishDB).values(
            data_to_insert,
        )
        await self._session.execute(stmt)

    async def commit(self) -> None:
        await self._session.commit()
