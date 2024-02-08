from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.infrastructure.database.models import Menu


class MenuUsecaseInterface(ABC):
    @abstractmethod
    async def get_menus(self) -> Sequence[Menu]:
        raise NotImplementedError

    @abstractmethod
    async def get_menus_with_all_data(self) -> Sequence[Menu]:
        raise NotImplementedError

    @abstractmethod
    async def get_menu(self, menu_id: UUID) -> Menu:
        raise NotImplementedError

    @abstractmethod
    async def create_menu(
        self,
        title: str,
        description: str,
    ) -> Menu:
        raise NotImplementedError

    @abstractmethod
    async def update_menu(
        self,
        menu_id: UUID,
        title: str | None,
        description: str | None,
    ) -> Menu:
        raise NotImplementedError

    @abstractmethod
    async def delete_menu(self, menu_id: UUID) -> None:
        raise NotImplementedError
