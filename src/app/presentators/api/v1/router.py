from fastapi import APIRouter

from app.presentators.api.v1.dish import router as dish_router
from app.presentators.api.v1.menu import router as menu_router
from app.presentators.api.v1.submenu import router as submenu_router

v1_router = APIRouter(prefix='/api/v1')

v1_router.include_router(dish_router)
v1_router.include_router(menu_router)
v1_router.include_router(submenu_router)
