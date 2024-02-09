from typing import Protocol
from uuid import UUID


class MenuCacheServiceInterface(Protocol):
    def get_menus(self) -> str | None:
        raise NotImplementedError

    def set_menus(self, menu_data: str) -> None:
        raise NotImplementedError

    def get_menu(
        self,
        menu_id: UUID,
    ) -> str | None:
        raise NotImplementedError

    def set_menu(
        self,
        menu_id: UUID,
        menu_data: str,
    ) -> None:
        raise NotImplementedError

    def get_menus_with_all_data(self) -> str | None:
        raise NotImplementedError

    def set_menus_with_all_data(self, menu_data: str) -> None:
        raise NotImplementedError

    def invalidate_cache_after_create_menu(self) -> None:
        raise NotImplementedError

    def invalidate_cache_after_update_menu(
        self,
        menu_id: UUID,
    ) -> None:
        raise NotImplementedError

    def invalidate_cache_after_delete_menu(
        self,
        menu_id: UUID,
    ) -> None:
        raise NotImplementedError

    def get_discount_for_dish(self, dish_id: UUID) -> int | float:
        raise NotImplementedError
