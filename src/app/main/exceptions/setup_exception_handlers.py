import logging
from functools import partial
from logging import config
from pathlib import Path
from typing import Callable

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.exceptions.dish import DishNotFound
from app.domain.exceptions.menu import MenuNotFound
from app.domain.exceptions.submenu import SubmenuNotFound
from app.main.config.logging import get_logging_dict

root_dir = '%s' % Path(__file__).parent.parent.parent

config.dictConfig(get_logging_dict(root_dir))
logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, unexpected_error_log)
    app.add_exception_handler(
        DishNotFound,
        get_error_handler('dish not found', 404),
    )
    app.add_exception_handler(
        MenuNotFound,
        get_error_handler('menu not found', 404),
    )
    app.add_exception_handler(
        SubmenuNotFound,
        get_error_handler('submenu not found', 404),
    )


def get_error_handler(error_info: str, status_code: int) -> Callable:
    return partial(
        error_handler,
        error_info=error_info,
        status_code=status_code,
    )


def error_handler(
    request: Request,
    ex: Exception,
    error_info: str,
    status_code: int,
) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status_code,
        content={'detail': error_info},
    )


async def unexpected_error_log(
    request: Request,
    ex: Exception,
) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content='Something went wrong',
    )
