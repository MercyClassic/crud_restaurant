from typing import Iterable, Protocol
from uuid import UUID

from app.application.synchronizer.models import Dish
from app.infrastructure.database.models import Dish as DishDB


class DishRepositoryInterface(Protocol):
    async def get_dishes(self) -> Iterable[DishDB]:
        raise NotImplementedError

    async def bulk_delete_dishes(self, dishes: Iterable[UUID]) -> None:
        raise NotImplementedError

    async def update_dish(self, dish: Dish) -> None:
        raise NotImplementedError

    async def bulk_insert_dishes(self, dishes: Iterable[Dish]) -> None:
        raise NotImplementedError
