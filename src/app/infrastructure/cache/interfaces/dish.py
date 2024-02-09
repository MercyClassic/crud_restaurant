from typing import Protocol
from uuid import UUID


class DishCacheServiceInterface(Protocol):
    def get_dishes(self) -> str | None:
        raise NotImplementedError

    def set_dishes(self, dish_data: str) -> None:
        raise NotImplementedError

    def get_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> str | None:
        raise NotImplementedError

    def set_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
        dish_data: str,
    ) -> None:
        raise NotImplementedError

    def get_discount_for_dish(self, dish_id: UUID) -> int | float:
        raise NotImplementedError

    def invalidate_cache_after_create_dish(
        self,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        raise NotImplementedError

    def invalidate_cache_after_update_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        raise NotImplementedError

    def invalidate_cache_after_delete_dish(
        self,
        dish_id: UUID,
        menu_id: UUID,
        submenu_id: UUID,
    ) -> None:
        raise NotImplementedError
