from uuid import UUID

from app.infrastructure.cache.services.redis.base import BaseRedisCacheService


class DishRedisCacheService(BaseRedisCacheService):
    def get_dishes(self) -> str | None:
        return self._cache.get('dishes')

    def set_dishes(self, dishes: str) -> None:
        self._cache.set('dishes', dishes, ex=30)

    def get_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> str | None:
        return self._cache.get(f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}')

    def set_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
        dish_data: str,
    ) -> None:
        self._cache.set(
            f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}',
            dish_data,
            ex=30,
        )

    def get_discount_for_dish(self, dish_id: UUID) -> int | float:
        return self._cache.get(f'discount_for_{dish_id}') or 0

    def invalidate_cache_after_create_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        self._cache.delete('dishes')
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')

    def invalidate_cache_after_update_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        self._cache.delete('dishes')
        self._cache.delete(f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}')

    def invalidate_cache_after_delete_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        self._cache.delete('dishes')
        self._cache.delete(f'dish-{dish_id}_submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('submenus')
        self._cache.delete(f'submenu-{submenu_id}_menu-{menu_id}')
        self._cache.delete('menus')
        self._cache.delete(f'menu-{menu_id}')
