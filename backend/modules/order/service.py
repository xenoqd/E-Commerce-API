from fastapi import HTTPException
from datetime import datetime, timedelta

from backend.modules.order.model import Order
from backend.modules.order.repository import OrderRepository
from backend.modules.order.events import OrderEvents
from backend.modules.cart.repository import CartRepository

from backend.core.event_bus import EventBus


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        cart_repo: CartRepository,
        event_bus: EventBus,
    ):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.event_bus = event_bus

    async def checkout(self, user_id: int):
        cart = await self.cart_repo.get_cart_by_user_id(user_id)
        items = await self.cart_repo.get_cart_items(cart.id)
        if not items:
            raise HTTPException(400, "No items in cart")

        order = Order(
            user_id=user_id,
            total_price=0,
            expires_at=datetime.utcnow() + timedelta(minutes=10),
        )

        order = await self.order_repo.create_order(order)

        await self.event_bus.publish(
            OrderEvents.ORDER_CREATED, {"order_id": order.id, "user_id": user_id}
        )
        return order

    async def get_user_orders(self, user_id: int):
        orders = await self.order_repo.get_orders_by_user(user_id)
        return orders

    async def get_order(self, order_id: int):
        order = await self.order_repo.get_order(order_id)
        return order
