from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from app.infrastructure.database.interfaces.repositories.sqlaclhemy_gateway import (
    SQLAlchemyBaseGateway,
)
from app.infrastructure.database.models.dish import Dish


class DishRepository(SQLAlchemyBaseGateway):
    async def get_dishes(self) -> Sequence[Dish]:
        query = select(Dish)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_dish(self, dish_id: UUID) -> Dish:
        query = select(Dish).where(Dish.id == dish_id)
        result = await self._session.execute(query)
        return result.scalar()

    async def save_dish(self, data: dict) -> Dish:
        stmt = insert(Dish).values(**data).returning(Dish)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def update_dish(self, dish_id: UUID, update_data: dict) -> Dish:
        stmt = update(Dish).where(Dish.id == dish_id).values(**update_data).returning(Dish)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_dish(self, dish_id: UUID) -> None:
        stmt = delete(Dish).where(Dish.id == dish_id)
        await self._session.execute(stmt)

    async def delete_dishes_by_submenu_id(self, submenu_id: UUID) -> None:
        stmt = delete(Dish).where(Dish.submenu_id == submenu_id)
        await self._session.execute(stmt)
