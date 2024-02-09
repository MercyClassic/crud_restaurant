from uuid import UUID

from app.infrastructure.cache.services.redis.base import BaseRedisCacheService


class SubmenuRedisCacheService(BaseRedisCacheService):
    def get_submenus(self) -> str | None:
        return self._cache.get('submenus')

    def set_submenus(self, submenus_data: str) -> None:
        self._cache.set('submenus', submenus_data, ex=30)

    def get_submenu(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> str | None:
        return self._cache.get(f'submenu-{submenu_id}_menu-{menu_id}')

    def set_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
        submenu_data: str,
    ) -> None:
        self._cache.set(
            f'submenu-{submenu_id}_menu-{menu_id}',
            submenu_data,
            ex=30,
        )

    def invalidate_cache_after_create_submenu(
        self,
        menu_id: UUID,
    ) -> None:
        self._cache.delete('submenus')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')

    def invalidate_cache_after_update_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}_menu-{menu_id}')

    def invalidate_cache_after_delete_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
        self._cache.delete('dishes')
        self.delete_by_pattern(f'dish-*_submenu-{submenu_id}_menu-{menu_id}')
