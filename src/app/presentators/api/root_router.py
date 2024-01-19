from fastapi import APIRouter

from app.presentators.api.v1.router import v1_router

root_router = APIRouter()
root_router.include_router(v1_router)


@root_router.get('/ping')
async def ping():
    return 'pong'
