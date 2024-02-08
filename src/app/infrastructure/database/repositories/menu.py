from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import joinedload, undefer

from app.infrastructure.database.interfaces.repositories.sqlaclhemy_gateway import (
    SQLAlchemyBaseGateway,
)
from app.infrastructure.database.models import Submenu
from app.infrastructure.database.models.menu import Menu


class MenuRepository(SQLAlchemyBaseGateway):
    async def get_menus(self) -> Sequence[Menu]:
        query = select(Menu).options(
            joinedload(Menu.submenus).load_only(Submenu.dishes_count),
        )
        result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def get_menus_with_all_data(self) -> Sequence[Menu]:
        query = select(Menu).options(
            joinedload(Menu.submenus).options(
                joinedload(Submenu.dishes),
            ),
        )
        result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def get_menu(self, menu_id: UUID) -> Menu | None:
        query = (
            select(Menu)
            .where(Menu.id == menu_id)
            .options(
                undefer(Menu.dishes_count),
                undefer(Menu.submenus_count),
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def save_menu(
        self,
        title: str,
        description: str,
    ) -> Menu:
        stmt = (
            insert(Menu)
            .values(
                title=title,
                description=description,
            )
            .returning(Menu)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def update_menu(
        self,
        menu_id: UUID,
        title: str | None = None,
        description: str | None = None,
    ) -> Menu | None:
        values = {}
        if title:
            values.update({'title': title})
        if description:
            values.update({'description': description})

        stmt = update(Menu).where(Menu.id == menu_id).values(**values).returning(Menu)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_menu(self, menu_id: UUID) -> None:
        stmt = delete(Menu).where(Menu.id == menu_id)
        await self._session.execute(stmt)
