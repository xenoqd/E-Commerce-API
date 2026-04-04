import asyncio
import redis.asyncio as redis
import traceback

from backend.core.config import settings
from backend.core.event_bus import EventBus
from backend.modules.order.events import OrderEvents
from backend.modules.order.service import OrderService
from backend.modules.order.handlers import OrderCreatedHandler
from backend.modules.order.repository import OrderRepository
from backend.modules.cart.repository import CartRepository
from backend.modules.products.repository import ProductsRepository
from backend.modules.cart.service import CartService
from backend.db.sync_db import get_async_session_maker


async def run_worker():
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        password=settings.REDIS_PASSWORD,
        decode_responses=False,
    )

    event_bus = EventBus(redis_client)
    session_maker = get_async_session_maker()

    async with session_maker() as session:
        cart_repo = CartRepository(session)
        product_repo = ProductsRepository(session)
        event_bus_for_services = event_bus

        order_service = OrderService(
            order_repo=OrderRepository(session),
            cart_repo=cart_repo,
            product_repo=product_repo,
            cart_service=CartService(
                repo=cart_repo,
                product_repo=product_repo,
                event_bus=event_bus_for_services
            ),
            event_bus=event_bus,
        )

        order_handler = OrderCreatedHandler(order_service=order_service)

    async def message_handler(msg_id, event_type, data):
        try:
            print(f"[EVENT] id={msg_id} type={event_type} data={data}")

            if event_type == OrderEvents.ORDER_CREATED:
                await order_handler.handle(msg_id, event_type, data)

        except Exception as e:
            print(f"[ERROR] Handler failed for msg_id={msg_id}: {e}")
            traceback.print_exc()

    print("[WORKER] Order worker started...")
    await event_bus.consume(
        group_name="order_group",
        consumer_name="order_worker_1",
        handler=message_handler
    )


if __name__ == "__main__":
    asyncio.run(run_worker())