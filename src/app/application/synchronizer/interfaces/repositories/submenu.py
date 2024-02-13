from typing import Iterable, Protocol
from uuid import UUID

from app.application.synchronizer.models import Submenu
from app.infrastructure.database.models import Submenu as SubmenuDB


class SubmenuRepositoryInterface(Protocol):
    async def get_submenus(self) -> Iterable[SubmenuDB]:
        raise NotImplementedError

    async def bulk_delete_submenus(self, menus: Iterable[UUID]) -> None:
        raise NotImplementedError

    async def update_submenu(self, menu: Submenu) -> None:
        raise NotImplementedError

    async def bulk_insert_submenus(self, submenus: Iterable[Submenu]) -> None:
        raise NotImplementedError
