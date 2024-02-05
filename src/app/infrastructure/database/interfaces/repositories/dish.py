from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Sequence
from uuid import UUID

from app.infrastructure.database.models.dish import Dish


class DishRepositoryInterface(ABC):
    @abstractmethod
    async def get_dishes(self) -> Sequence[Dish]:
        raise NotImplementedError

    @abstractmethod
    async def get_dish(self, dish_id: UUID) -> Dish | None:
        raise NotImplementedError

    @abstractmethod
    async def save_dish(
        self,
        submenu_id: UUID,
        title: str,
        description: str,
        price: Decimal,
    ) -> Dish:
        raise NotImplementedError

    @abstractmethod
    async def update_dish(
        self,
        dish_id: UUID,
        title: str | None,
        description: str | None,
        price: Decimal | None,
    ) -> Dish:
        raise NotImplementedError

    @abstractmethod
    async def delete_dish(self, dish_id: UUID) -> None:
        raise NotImplementedError
