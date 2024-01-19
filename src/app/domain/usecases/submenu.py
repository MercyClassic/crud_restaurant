from uuid import UUID

from app.domain.exceptions.submenu import SubmenuNotFound
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


class SubmenuUsecase:
    def __init__(self, uow: UoWInterface):
        self.uow = uow

    async def get_submenus(self):
        return await self.uow.submenu_repo.get_submenus()

    async def get_submenu(self, submenu_id: UUID):
        submenu = await self.uow.submenu_repo.get_submenu(submenu_id)
        if not submenu:
            raise SubmenuNotFound
        return submenu

    async def create_submenu(self, menu_id: UUID, submenu_data: dict):
        submenu_data['menu_id'] = menu_id
        submenu = await self.uow.submenu_repo.save_submenu(submenu_data)
        await self.uow.commit()
        submenu = await self.uow.submenu_repo.get_submenu(submenu.id)
        return submenu

    async def update_submenu(self, submenu_id: UUID, submenu_data: dict):
        submenu = await self.uow.submenu_repo.update_submenu(submenu_id, submenu_data)
        await self.uow.commit()
        submenu = await self.uow.submenu_repo.get_submenu(submenu.id)
        return submenu

    async def delete_submenu(self, submenu_id: UUID):
        await self.uow.dish_repo.delete_dishes_by_submenu_id(submenu_id)
        await self.uow.submenu_repo.delete_submenu(submenu_id)
        await self.uow.commit()
