from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.infrastructure.database.models.submenu import Submenu


class SubRepositoryInterface(ABC):
    @abstractmethod
    async def get_submenus(self) -> List[Submenu]:
        raise NotImplementedError

    @abstractmethod
    async def get_submenu(self, submenu_id: UUID) -> Submenu:
        raise NotImplementedError

    @abstractmethod
    async def save_submenu(self, data: dict) -> Submenu:
        raise NotImplementedError

    @abstractmethod
    async def update_submenu(self, submenu_id: UUID, update_data: dict) -> Submenu:
        raise NotImplementedError

    @abstractmethod
    async def delete_submenu(self, submenu_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_submenus_by_menu_id(self, menu_id: UUID) -> None:
        raise NotImplementedError
