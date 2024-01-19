from abc import ABC, abstractmethod
from uuid import UUID


class SubmenuUsecaseInterface(ABC):
    @abstractmethod
    async def get_submenus(self):
        raise NotImplementedError

    @abstractmethod
    async def get_submenu(self, submenu_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def create_submenu(self, menu_id: UUID, submenu_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_submenu(self, submenu_id: UUID, submenu_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_submenu(self, submenu_id: UUID):
        raise NotImplementedError
