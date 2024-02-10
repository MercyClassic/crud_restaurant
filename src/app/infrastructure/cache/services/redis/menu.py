from uuid import UUID

from app.infrastructure.cache.services.redis.base import BaseRedisCacheService


class MenuRedisCacheService(BaseRedisCacheService):
    def get_menus(self) -> str | None:
        return self._cache.get('menus')

    def set_menus(self, menu_data: str) -> None:
        self._cache.set('menus', menu_data, ex=30)

    def get_menu(
        self,
        menu_id: UUID,
    ) -> str | None:
        return self._cache.get(f'menu-{menu_id}')

    def set_menu(
        self,
        menu_id: UUID,
        menu_data: str,
    ) -> None:
        self._cache.set(f'menu-{menu_id}', menu_data, ex=30)

    def get_menus_with_all_data(self) -> str | None:
        return self._cache.get('menus-all-data')

    def set_menus_with_all_data(self, menu_data: str) -> str | None:
        return self._cache.set('menus-all-data', menu_data, ex=30)

    def invalidate_cache_after_create_menu(self) -> None:
        self._cache.delete('menus')

    def invalidate_cache_after_update_menu(
        self,
        menu_id: UUID,
    ) -> None:
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')

    def invalidate_cache_after_delete_menu(
        self,
        menu_id: UUID,
    ) -> None:
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
        self._cache.delete('submenus')
        self._cache.delete('dishes')
        self.delete_by_pattern(f'submenu-*_menu-{menu_id}')
        self.delete_by_pattern(f'dish-*_submenu-*_menu-{menu_id}')

    def get_discount_for_dish(self, dish_id: UUID) -> float:
        return float(self._cache.get(f'discount_for_{dish_id}') or 0)
