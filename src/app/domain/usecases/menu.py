from uuid import UUID

from app.domain.exceptions.menu import MenuNotFound
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


class MenuUsecase:
    def __init__(self, uow: UoWInterface):
        self.uow = uow

    async def get_menus(self):
        return await self.uow.menu_repo.get_menus()

    async def get_menu(self, menu_id: UUID):
        menu = await self.uow.menu_repo.get_menu(menu_id)
        if not menu:
            raise MenuNotFound
        return menu

    async def create_menu(self, menu_data: dict):
        menu = await self.uow.menu_repo.save_menu(menu_data)
        await self.uow.commit()
        menu = await self.uow.menu_repo.get_menu(menu.id)
        return menu

    async def update_menu(self, menu_id: UUID, menu_data: dict):
        menu = await self.uow.menu_repo.update_menu(menu_id, menu_data)
        await self.uow.commit()
        menu = await self.uow.menu_repo.get_menu(menu.id)
        return menu

    async def delete_menu(self, menu_id: UUID):
        await self.uow.submenu_repo.delete_submenus_by_menu_id(menu_id)
        await self.uow.menu_repo.delete_menu(menu_id)
        await self.uow.commit()
