from backend.core.builder import build_event_bus

from backend.modules.cart.service import CartService
from backend.modules.cart.repository import CartRepository
from backend.modules.products.repository import ProductsRepository
from backend.modules.order.handlers import OrderHandlers
from backend.modules.order.repository import OrderRepository

from sqlalchemy.ext.asyncio import AsyncSession


class OrderProcessor:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.cart_repo = CartRepository(session)
        self.product_repo = ProductsRepository(session)

        event_bus = build_event_bus()

        self.cart_service = CartService(
            repo=self.cart_repo, product_repo=self.product_repo, event_bus=event_bus
        )

        self.handler = OrderHandlers(
            self.order_repo, self.cart_repo, self.product_repo, self.cart_service
        )

    async def process_order_created(self, data: dict):
        await self.handler.handle_order_created(data)
