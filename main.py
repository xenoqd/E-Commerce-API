from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.db.init import db_lifespan
from backend.infrastructure.redis.lifespan import redis_lifespan
from backend.modules.users.api import register_router


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with redis_lifespan(app):
        async with db_lifespan(app):
            print("All resources are initialized")
            yield
            print("All resources closed")


app = FastAPI(lifespan=app_lifespan)
app.include_router(register_router)