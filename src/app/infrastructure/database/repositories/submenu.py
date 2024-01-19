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
            undefer(Submenu.dish_count),
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_submenu(self, submenu_id: UUID) -> Submenu:
        query = (
            select(Submenu)
            .where(Submenu.id == submenu_id)
            .options(
                undefer(Submenu.dish_count),
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def save_submenu(self, data: dict) -> Submenu:
        stmt = insert(Submenu).values(**data).returning(Submenu)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def update_submenu(self, submenu_id: UUID, update_data: dict) -> Submenu:
        stmt = (
            update(Submenu).where(Submenu.id == submenu_id).values(**update_data).returning(Submenu)
        )
        result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_submenu(self, submenu_id: UUID) -> None:
        stmt = delete(Submenu).where(Submenu.id == submenu_id)
        await self._session.execute(stmt)

    async def delete_submenus_by_menu_id(self, menu_id: UUID) -> None:
        stmt = delete(Submenu).where(Submenu.menu_id == menu_id)
        await self._session.execute(stmt)
