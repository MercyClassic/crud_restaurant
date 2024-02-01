from sqlalchemy.ext.asyncio import AsyncSession


async def get_session_stub() -> AsyncSession:
    raise NotImplementedError
