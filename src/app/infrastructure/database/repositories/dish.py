from decimal import Decimal
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

    async def get_dish(self, dish_id: UUID) -> Dish | None:
        query = select(Dish).where(Dish.id == dish_id)
        result = await self._session.execute(query)
        return result.scalar()

    async def save_dish(
        self,
        submenu_id: UUID,
        title: str,
        description: str,
        price: Decimal,
    ) -> Dish:
        stmt = (
            insert(Dish)
            .values(
                submenu_id=submenu_id,
                title=title,
                description=description,
                price=price,
            )
            .returning(Dish)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def update_dish(
        self,
        dish_id: UUID,
        title: str | None = None,
        description: str | None = None,
        price: Decimal | None = None,
    ) -> Dish | None:
        values = {}
        if title:
            values.update({'title': title})
        if description:
            values.update({'description': description})
        if price:
            values.update({'price': str(price)})

        stmt = update(Dish).where(Dish.id == dish_id).values(**values).returning(Dish)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_dish(self, dish_id: UUID) -> None:
        stmt = delete(Dish).where(Dish.id == dish_id)
        await self._session.execute(stmt)
