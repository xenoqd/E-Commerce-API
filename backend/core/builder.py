import redis.asyncio as redis

from backend.core.config import settings
from backend.core.event_bus import EventBus

def build_event_bus() -> EventBus:
    redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            password=settings.REDIS_PASSWORD,
            decode_responses=False,
        )

    return EventBus(redis_client)