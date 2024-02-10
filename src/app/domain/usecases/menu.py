import json
from typing import Sequence
from uuid import UUID

from app.application.encoders.json import JSONEncoder
from app.domain.exceptions.menu import MenuNotFound
from app.infrastructure.cache.interfaces.menu import MenuCacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.infrastructure.database.models import Menu


class MenuUsecase:
    def __init__(
        self,
        uow: UoWInterface,
        cache: MenuCacheServiceInterface,
    ):
        self._uow = uow
        self._cache = cache

    async def get_menus(self) -> Sequence[Menu]:
        menus = self._cache.get_menus()
        if not menus:
            menus = await self._uow.menu_repo.get_menus()
            encoder = JSONEncoder(menus)
            menus = encoder.data
            self._cache.set_menus(json.dumps(menus))
        else:
            menus = json.loads(menus)
        return menus

    def _synchronize_dish_prices(self, menus: list[dict]) -> None:
        for menu in menus:
            for submenu in menu.get('submenus', []):
                for dish in submenu.get('dishes', []):
                    dish['price'] *= 1 - self._cache.get_discount_for_dish(dish['id']) / 100

    async def get_menus_with_all_data(self) -> Sequence[Menu]:
        menus = self._cache.get_menus_with_all_data()
        if not menus:
            menus = await self._uow.menu_repo.get_menus_with_all_data()
            encoder = JSONEncoder(menus)
            menus = encoder.data
            self._synchronize_dish_prices(menus)
            self._cache.set_menus_with_all_data(json.dumps(menus))
        else:
            menus = json.loads(menus)
        return menus

    async def get_menu(self, menu_id: UUID) -> Menu:
        menu = self._cache.get_menu(menu_id)
        if not menu:
            menu = await self._uow.menu_repo.get_menu(menu_id)
            if not menu:
                raise MenuNotFound
            encoder = JSONEncoder(menu)
            menu = encoder.data
            self._cache.set_menu(menu_id, json.dumps(menu))
        else:
            menu = json.loads(menu)
        return menu

    async def create_menu(
        self,
        title: str,
        description: str,
    ) -> Menu:
        menu = await self._uow.menu_repo.save_menu(
            title=title,
            description=description,
        )
        await self._uow.commit()
        menu = await self._uow.menu_repo.get_menu(menu.id)
        return menu

    async def update_menu(
        self,
        menu_id: UUID,
        title: str | None,
        description: str | None,
    ) -> Menu:
        menu = await self._uow.menu_repo.update_menu(
            menu_id=menu_id,
            title=title,
            description=description,
        )
        await self._uow.commit()
        menu = await self._uow.menu_repo.get_menu(menu.id)
        return menu

    async def delete_menu(self, menu_id: UUID) -> None:
        await self._uow.menu_repo.delete_menu(menu_id)
        await self._uow.commit()
