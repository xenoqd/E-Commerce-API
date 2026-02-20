from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


def get_db_session_factory(request: Request):
    factory = request.app.state.db_session_factory
    if factory is None:
        raise RuntimeError("DB session factory not initialized")
    return factory


async def get_session(factory=Depends(get_db_session_factory)) -> AsyncSession:
    async with factory() as session:
        yield session