from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any, ex: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def _delete_by_pattern(self, pattern: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_dish(
        self,
        dish_id: UUID,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete_menu(self, menu_id: UUID) -> Any:
        raise NotImplementedError
