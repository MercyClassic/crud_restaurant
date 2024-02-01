from fastapi import APIRouter

from app.presentators.api.v1.router import v1_router

root_router = APIRouter()
root_router.include_router(v1_router)


@root_router.get(
    '/ping',
    response_model=str,
    status_code=200,
    tags=['healthcheck'],
    description='App available check',
)
async def ping() -> str:
    return 'pong'
