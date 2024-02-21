from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.infrastructure.database.models import Submenu


class SubmenuServiceInterface(ABC):
    @abstractmethod
    async def get_submenus(self) -> Sequence[Submenu]:
        raise NotImplementedError

    @abstractmethod
    async def get_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> Submenu:
        raise NotImplementedError

    @abstractmethod
    async def create_submenu(
        self,
        menu_id: UUID,
        title: str,
        description: str,
    ) -> Submenu:
        raise NotImplementedError

    @abstractmethod
    async def update_submenu(
        self,
        submenu_id: UUID,
        title: str | None,
        description: str | None,
    ) -> Submenu:
        raise NotImplementedError

    @abstractmethod
    async def delete_submenu(
        self,
        submenu_id: UUID,
    ) -> None:
        raise NotImplementedError
