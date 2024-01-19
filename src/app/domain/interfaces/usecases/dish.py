from abc import ABC, abstractmethod
from uuid import UUID


class DishUsecaseInterface(ABC):
    @abstractmethod
    async def get_dishes(self):
        raise NotImplementedError

    @abstractmethod
    async def create_dish(self, submenu_id: UUID, dish_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_dish(self, dish_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def update_dish(self, dish_id: UUID, update_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_dish(self, dish_id: UUID):
        raise NotImplementedError
