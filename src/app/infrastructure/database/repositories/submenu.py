from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import undefer

from app.infrastructure.database.interfaces.repositories.sqlaclhemy_gateway import (
    SQLAlchemyBaseGateway,
)
from app.infrastructure.database.models.submenu import Submenu


class SubmenuRepository(SQLAlchemyBaseGateway):
    async def get_submenus(self) -> Sequence[Submenu]:
        query = select(Submenu).options(
            undefer(Submenu.dishes_count),
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_submenu(self, submenu_id: UUID) -> Submenu | None:
        query = (
            select(Submenu)
            .where(Submenu.id == submenu_id)
            .options(
                undefer(Submenu.dishes_count),
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def save_submenu(
        self,
        menu_id: UUID,
        title: str,
        description: str,
    ) -> Submenu:
        stmt = (
            insert(Submenu)
            .values(
                menu_id=menu_id,
                title=title,
                description=description,
            )
            .returning(Submenu)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def update_submenu(
        self,
        submenu_id: UUID,
        title: str | None = None,
        description: str | None = None,
    ) -> Submenu | None:
        values = {}
        if title:
            values.update({'title': title})
        if description:
            values.update({'description': description})

        stmt = update(Submenu).where(Submenu.id == submenu_id).values(**values).returning(Submenu)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_submenu(self, submenu_id: UUID) -> None:
        stmt = delete(Submenu).where(Submenu.id == submenu_id)
        await self._session.execute(stmt)
