from typing import Any
from uuid import UUID


class RedisCacheService:
    def __init__(self, cache: Any):
        self._cache = cache

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any, ex: int | None = None) -> None:
        self._cache.set(key, value, ex)

    def delete(self, key: str) -> None:
        self._cache.delete(key)

    def _delete_by_pattern(self, pattern: str) -> None:
        keys = self._cache.keys(f'*{pattern}*')
        for key in keys:
            self._cache.delete(key)

    def delete_dish(
        self,
        dish_id: UUID,
        submenu_id: UUID,
        menu_id: UUID,
    ):
        self._cache.delete('dishes')
        self._cache.delete(f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')

    def delete_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ):
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
        self._cache.delete('dishes')
        self._delete_by_pattern(f'dish-*_submenu-{submenu_id}_menu-{menu_id}')

    def delete_menu(self, menu_id: UUID):
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
        self._cache.delete('submenus')
        self._cache.delete('dishes')
        self._delete_by_pattern(f'submenu-*_menu-{menu_id}')
        self._delete_by_pattern(f'dish-*_submenu-*_menu-{menu_id}')
