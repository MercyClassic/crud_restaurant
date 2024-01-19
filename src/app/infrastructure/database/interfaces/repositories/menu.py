from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.infrastructure.database.models.menu import Menu


class MenuRepositoryInterface(ABC):
    @abstractmethod
    async def get_menus(self) -> List[Menu]:
        raise NotImplementedError

    @abstractmethod
    async def get_menu(self, menu_id: UUID) -> Menu:
        raise NotImplementedError

    @abstractmethod
    async def save_menu(self, data: dict) -> Menu:
        raise NotImplementedError

    @abstractmethod
    async def update_menu(self, menu_id: UUID, update_data: dict) -> Menu:
        raise NotImplementedError

    @abstractmethod
    async def delete_menu(self, menu_id: UUID) -> None:
        raise NotImplementedError
