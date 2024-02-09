from typing import Protocol
from uuid import UUID


class SubmenuCacheServiceInterface(Protocol):
    def get_submenus(self) -> str | None:
        raise NotImplementedError

    def set_submenus(self, submenus_data: str) -> None:
        raise NotImplementedError

    def get_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> str | None:
        raise NotImplementedError

    def set_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
        submenu_data: str,
    ) -> None:
        raise NotImplementedError

    def invalidate_cache_after_create_submenu(
        self,
        menu_id: UUID,
    ) -> None:
        raise NotImplementedError

    def invalidate_cache_after_update_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        raise NotImplementedError

    def invalidate_cache_after_delete_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> None:
        raise NotImplementedError
