from sqlalchemy import create_engine
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