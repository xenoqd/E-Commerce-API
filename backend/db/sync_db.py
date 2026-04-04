from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from backend.core.config import settings

_sync_engine = None

def get_sync_engine():
    global _sync_engine
    if _sync_engine is None:
        url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://")

        _sync_engine = create_engine(
            url,
            pool_pre_ping=True,
            poolclass=NullPool,
            pool_recycle=1800,
        )
    return _sync_engine


_async_engine = None
async_session_maker = None

def init_async_engine_and_sessionmaker():
    global _async_engine, async_session_maker
    if _async_engine is None:
        _async_engine = create_async_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            poolclass=NullPool,
            pool_recycle=1800,
            # echo=settings.DEBUG,
        )
        async_session_maker = async_sessionmaker(
            _async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )


def get_async_session_maker():
    if async_session_maker is None:
        init_async_engine_and_sessionmaker()
    return async_session_maker