from typing import Iterable, Protocol
from uuid import UUID

from app.application.synchronizer.models import Menu
from app.infrastructure.database.models import Menu as MenuDB


class MenuRepositoryInterface(Protocol):
    async def get_menus(self) -> Iterable[MenuDB]:
        raise NotImplementedError

    async def bulk_delete_menus(self, menus: Iterable[UUID]) -> None:
        raise NotImplementedError

    async def update_menu(self, menu: Menu) -> None:
        raise NotImplementedError

    async def bulk_insert_menus(self, menus: Iterable[Menu]) -> None:
        raise NotImplementedError
