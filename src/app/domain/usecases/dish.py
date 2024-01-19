from uuid import UUID

from app.domain.exceptions.dish import DishNotFound
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


class DishUsecase:
    def __init__(self, uow: UoWInterface):
        self.uow = uow

    async def get_dishes(self):
        return await self.uow.dish_repo.get_dishes()

    async def get_dish(self, dish_id: UUID):
        dish = await self.uow.dish_repo.get_dish(dish_id)
        if not dish:
            raise DishNotFound
        return dish

    async def create_dish(self, submenu_id: int, dish_data: dict):
        dish_data['submenu_id'] = submenu_id
        dish = await self.uow.dish_repo.save_dish(dish_data)
        await self.uow.commit()
        return dish

    async def update_dish(self, dish_id: UUID, dish_data: dict):
        dish = await self.uow.dish_repo.update_dish(dish_id, dish_data)
        await self.uow.commit()
        return dish

    async def delete_dish(self, dish_id: UUID):
        await self.uow.dish_repo.delete_dish(dish_id)
        await self.uow.commit()
