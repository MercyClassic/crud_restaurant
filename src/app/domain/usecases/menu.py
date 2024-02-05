import json
from typing import Sequence
from uuid import UUID

from app.application.encoders.json import JSONEncoder
from app.domain.exceptions.menu import MenuNotFound
from app.infrastructure.cache.interface import CacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.infrastructure.database.models import Menu


class MenuUsecase:
    def __init__(
        self,
        uow: UoWInterface,
        cache: CacheServiceInterface,
    ):
        self._uow = uow
        self._cache = cache

    async def get_menus(self) -> Sequence[Menu]:
        menus = self._cache.get('menus')
        if not menus:
            menus = await self._uow.menu_repo.get_menus()
            encoder = JSONEncoder(menus)
            menus = encoder.data
            self._cache.set('menus', json.dumps(menus), ex=30)
        else:
            menus = json.loads(menus)
        return menus

    async def get_menu(self, menu_id: UUID) -> Menu:
        menu = self._cache.get(f'menu-{menu_id}')
        if not menu:
            menu = await self._uow.menu_repo.get_menu(menu_id)
            if not menu:
                raise MenuNotFound
            encoder = JSONEncoder(menu)
            menu = encoder.data
            self._cache.set(f'menu-{menu_id}', json.dumps(menu), ex=30)
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
        self._cache.delete('menus')
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
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
        return menu

    async def delete_menu(self, menu_id: UUID) -> None:
        await self._uow.menu_repo.delete_menu(menu_id)
        await self._uow.commit()
        self._invalidate_cache_after_delete_menu(menu_id)

    def _invalidate_cache_after_delete_menu(self, menu_id: UUID):
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
        self._cache.delete('submenus')
        self._cache.delete('dishes')
        self._cache.delete_by_pattern(f'submenu-*_menu-{menu_id}')
        self._cache.delete_by_pattern(f'dish-*_submenu-*_menu-{menu_id}')
