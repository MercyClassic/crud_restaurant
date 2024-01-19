from abc import ABC, abstractmethod
from uuid import UUID


class MenuUsecaseInterface(ABC):
    @abstractmethod
    async def get_menus(self):
        raise NotImplementedError

    @abstractmethod
    async def get_menu(self, menu_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def create_menu(self, menu_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_menu(self, menu_id: UUID, menu_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_menu(self, menu_id: UUID):
        raise NotImplementedError
