from typing import Iterable
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.synchronizer.models import Dish
from app.infrastructure.database.models import Dish as DishDB


class DishRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def _convert_dishes(self, dishes: Iterable[Dish]):
        return [
            {
                'id': dish.id,
                'title': dish.title,
                'description': dish.description,
                'price': dish.price,
                'submenu_id': dish.submenu_id,
            }
            for dish in dishes
        ]

    async def get_dishes(self) -> Iterable[DishDB]:
        result = await self._session.execute(select(DishDB))
        return result.scalars().all()

    async def bulk_delete_dishes(self, dishes: Iterable[UUID]) -> None:
        stmt = delete(DishDB).where(DishDB.id.in_(dishes))
        await self._session.execute(stmt)

    async def update_dish(self, dish: Dish) -> None:
        stmt = (
            update(DishDB)
            .values(
                title=dish.title,
                description=dish.description,
                price=dish.price,
                submenu_id=dish.submenu_id,
            )
            .where(DishDB.id == dish.id)
        )
        await self._session.execute(stmt)

    async def bulk_insert_dishes(self, dishes: Iterable[Dish]) -> None:
        data_to_insert = self._convert_dishes(dishes)
        stmt = insert(DishDB).values(
            data_to_insert,
        )
        await self._session.execute(stmt)
