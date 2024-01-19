from fastapi import FastAPI

from app.main.di.init_dependencies import init_dependencies
from app.main.exceptions.setup_exception_handlers import setup_exception_handlers
from app.presentators.api.root_router import root_router


def create_app() -> FastAPI:
    app = FastAPI()
    setup_exception_handlers(app)
    init_dependencies(app)
    app.include_router(root_router)
    return app


app = create_app()
