from abc import abstractmethod
from typing import Iterable, Protocol

from app.application.synchronizer.models import Dish, Menu, Submenu


class SyncRepositoryInterface(Protocol):
    @abstractmethod
    async def clear_db(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def bulk_insert_menus(self, menus: Iterable[Menu]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def bulk_insert_submenus(self, submenus: Iterable[Submenu]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def bulk_insert_dishes(self, dishes: Iterable[Dish]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
