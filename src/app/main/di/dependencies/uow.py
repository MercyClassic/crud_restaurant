from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.uow import UoW
from app.main.di.stub import get_session_stub


async def get_uow(
    session: Annotated[AsyncSession, Depends(get_session_stub)],
) -> UoW:
    return UoW(session)
