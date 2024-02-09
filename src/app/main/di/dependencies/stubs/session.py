from sqlalchemy.ext.asyncio import AsyncSession


def get_session_stub() -> AsyncSession:
    raise NotImplementedError
