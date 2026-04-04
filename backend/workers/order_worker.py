import asyncio
import redis.asyncio as redis

from backend.core.config import settings
from backend.core.event_bus import EventBus
from backend.modules.order.events import OrderEvents
from backend.modules.order.processors import OrderProcessor
from backend.db.sync_db import get_async_session_maker

import traceback


async def run_worker():
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        password=settings.REDIS_PASSWORD,
        decode_responses=False,
    )

    event_bus = EventBus(redis_client)

    async def handler(msg_id, event_type, data):
        try:
            print(f"[EVENT] id={msg_id} type={event_type} data={data}")

            if event_type == OrderEvents.ORDER_CREATED:
                session_maker = get_async_session_maker()
                async with session_maker() as session:
                    try:
                        processor = OrderProcessor(session=session)
                        await processor.process_order_created(data)
                        await session.commit()
                    except Exception as e:
                        await session.rollback()
                        print(
                            f"[ERROR]: {e} Failed to process order {data.get('order_id')}"
                        )

        except Exception as e:
            print(f"[ERROR] Handler failed for msg_id={msg_id}")
            print(f"[ERROR] Type: {type(e).__name__}")
            print(f"[ERROR] Message: {e}")
            print("[TRACEBACK]")
            traceback.print_exc()

    await event_bus.consume(
        group_name="order_group", consumer_name="order_worker_1", handler=handler
    )


if __name__ == "__main__":
    asyncio.run(run_worker())
