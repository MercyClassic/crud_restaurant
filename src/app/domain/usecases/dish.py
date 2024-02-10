import json
from decimal import Decimal
from typing import Sequence
from uuid import UUID

from app.application.encoders.json import JSONEncoder
from app.domain.exceptions.dish import DishNotFound
from app.infrastructure.cache.interfaces.dish import DishCacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.infrastructure.database.models import Dish


class DishUsecase:
    def __init__(
        self,
        uow: UoWInterface,
        cache: DishCacheServiceInterface,
    ):
        self._uow = uow
        self._cache = cache

    async def get_dishes(self) -> Sequence[Dish]:
        dishes = self._cache.get_dishes()
        if not dishes:
            dishes = await self._uow.dish_repo.get_dishes()
            encoder = JSONEncoder(dishes)
            dishes = encoder.data
            for dish in dishes:
                dish['price'] *= 1 - self._cache.get_discount_for_dish(dish['id']) / 100
            self._cache.set_dishes(json.dumps(dishes))
        else:
            dishes = json.loads(dishes)
        return dishes

    async def get_dish(
        self,
        dish_id: UUID,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> Dish:
        dish = self._cache.get_dish(dish_id, submenu_id, menu_id)
        if not dish:
            dish = await self._uow.dish_repo.get_dish(dish_id)
            if not dish:
                raise DishNotFound
            encoder = JSONEncoder(dish)
            dish = encoder.data
            dish['price'] *= 1 - self._cache.get_discount_for_dish(dish['id']) / 100
            self._cache.set_dish(dish_id, submenu_id, menu_id, dish_data=json.dumps(dish))
        else:
            dish = json.loads(dish)
        return dish

    async def create_dish(
        self,
        submenu_id: UUID,
        title: str,
        description: str,
        price: Decimal,
    ) -> Dish:
        dish = await self._uow.dish_repo.save_dish(
            submenu_id=submenu_id,
            title=title,
            description=description,
            price=price,
        )
        await self._uow.commit()
        return dish

    async def update_dish(
        self,
        dish_id: UUID,
        title: str | None,
        description: str | None,
        price: Decimal | None,
    ) -> Dish:
        dish = await self._uow.dish_repo.update_dish(
            dish_id=dish_id,
            title=title,
            description=description,
            price=price,
        )
        await self._uow.commit()
        return dish

    async def delete_dish(
        self,
        dish_id: UUID,
    ) -> None:
        await self._uow.dish_repo.delete_dish(dish_id)
        await self._uow.commit()
