from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.infrastructure.database.models.dish import Dish


class DishRepositoryInterface(ABC):
    @abstractmethod
    async def get_dishes(self) -> List[Dish]:
        raise NotImplementedError

    @abstractmethod
    async def get_dish(self, dish_id: UUID) -> Dish:
        raise NotImplementedError

    @abstractmethod
    async def save_dish(self, data: dict) -> Dish:
        raise NotImplementedError

    @abstractmethod
    async def update_dish(self, dish_id: UUID, update_data: dict) -> Dish:
        raise NotImplementedError

    @abstractmethod
    async def delete_dish(self, dish_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_dishes_by_submenu_id(self, submenu_id: UUID) -> None:
        raise NotImplementedError
