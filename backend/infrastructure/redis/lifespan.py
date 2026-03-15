from contextlib import asynccontextmanager
from fastapi import FastAPI

import redis.asyncio as redis
from backend.core.config import settings
from backend.core.event_bus import EventBus


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=False,
        password=settings.REDIS_PASSWORD
    )

    try:
        await client.ping()
        print("Redis connected succefully")
    except Exception as e:
        print(f"Redis not available: {e}")
        raise

    app.state.redis_client = client
    app.state.event_bus = EventBus(client)

    yield

    print("Closing Redis...")
    await client.aclose()
