import asyncio
import os
from functools import partial
from typing import Any, AsyncGenerator, Generator, Iterable

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.infrastructure.database.models import Base
from app.main.di.dependencies.stubs.cache import CacheInstance
from app.main.di.dependencies.stubs.session import get_session_stub
from app.main.main import app

test_engine = create_async_engine(os.environ['test_db_uri'], poolclass=NullPool)
Base.metadata.bind = test_engine


def reverse(path: str, **path_params) -> str:
    return app.url_path_for(path, **path_params)


def create_test_async_session_maker(test_engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_test_async_session(
    test_async_session_maker: async_sessionmaker,
) -> AsyncGenerator:
    async with test_async_session_maker() as session:
        yield session


class CacheMock:
    def get(self, *args, **kwargs) -> Any:
        pass

    def set(self, *args, **kwargs) -> Any:
        pass

    def delete(self, *args, **kwargs) -> Any:
        pass

    def delete_by_pattern(self, *args, **kwargs) -> Any:
        pass

    def keys(self, *args, **kwargs) -> Iterable:
        return []


def get_cache_mock():
    return CacheMock()


test_async_session_maker = create_test_async_session_maker(test_engine)

app.dependency_overrides[get_session_stub] = partial(
    get_test_async_session,
    test_async_session_maker,
)
app.dependency_overrides[CacheInstance] = get_cache_mock


@pytest.fixture(autouse=True, scope='function')
async def prepare_database() -> AsyncGenerator[None, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request) -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture()
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session
