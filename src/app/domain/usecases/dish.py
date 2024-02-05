import json
from decimal import Decimal
from typing import Sequence
from uuid import UUID

from app.application.encoders.json import JSONEncoder
from app.domain.exceptions.dish import DishNotFound
from app.infrastructure.cache.interface import CacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.infrastructure.database.models import Dish


class DishUsecase:
    def __init__(
        self,
        uow: UoWInterface,
        cache: CacheServiceInterface,
    ):
        self._uow = uow
        self._cache = cache

    async def get_dishes(self) -> Sequence[Dish]:
        dishes = self._cache.get('dishes')
        if not dishes:
            dishes = await self._uow.dish_repo.get_dishes()
            encoder = JSONEncoder(dishes)
            dishes = encoder.data
            self._cache.set('dishes', json.dumps(dishes), ex=30)
        else:
            dishes = json.loads(dishes)
        return dishes

    async def get_dish(
        self,
        dish_id: UUID,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> Dish:
        dish = self._cache.get(f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}')
        if not dish:
            dish = await self._uow.dish_repo.get_dish(dish_id)
            if not dish:
                raise DishNotFound
            encoder = JSONEncoder(dish)
            dish = encoder.data
            self._cache.set(
                f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}',
                json.dumps(dish),
                ex=30,
            )
        else:
            dish = json.loads(dish)
        return dish

    async def create_dish(
        self,
        submenu_id: UUID,
        menu_id: UUID,
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
        self._cache.delete('dishes')
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
        return dish

    async def update_dish(
        self,
        dish_id: UUID,
        submenu_id: UUID,
        menu_id: UUID,
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
        self._cache.delete('dishes')
        self._cache.delete(f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}')
        return dish

    async def delete_dish(
        self,
        dish_id: UUID,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        await self._uow.dish_repo.delete_dish(dish_id)
        await self._uow.commit()
        self._cache.delete('dishes')
        self._cache.delete(f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
