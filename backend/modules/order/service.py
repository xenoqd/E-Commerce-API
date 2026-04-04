from fastapi import HTTPException
from datetime import datetime, timedelta

from backend.modules.order.model import Order, OrderItem
from backend.modules.order.repository import OrderRepository
from backend.modules.order.events import OrderEvents
from backend.modules.cart.repository import CartRepository
from backend.modules.cart.service import CartService
from backend.modules.products.repository import ProductsRepository
from backend.db.sync_db import get_async_session_maker

from backend.core.event_bus import EventBus

class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        cart_repo: CartRepository,
        product_repo: ProductsRepository,
        cart_service: CartService,
        event_bus: EventBus,
    ):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.product_repo = product_repo
        self.cart_service = cart_service
        self.event_bus = event_bus
        self.session_maker = get_async_session_maker()

    async def checkout(self, user_id: int):
        cart = await self.cart_repo.get_cart_by_user_id(user_id)
        items = await self.cart_repo.get_cart_items(cart.id) if cart else []

        if not items:
            raise HTTPException(status_code=400, detail="No items in cart")

        order = Order(
            user_id=user_id,
            total_price=0,
            expires_at=datetime.utcnow() + timedelta(minutes=10),
        )

        order = await self.order_repo.create_order(order)

        await self.event_bus.publish(
            OrderEvents.ORDER_CREATED, 
            {"order_id": order.id, "user_id": user_id}
        )
        return order

    async def process_order_created(self, order_id: int, user_id: int):
        print(f"[INFO] Start processing order_id={order_id} user_id={user_id}")

        async with self.session_maker() as session:
            try:
                order_repo = OrderRepository(session)
                cart_repo = CartRepository(session)
                product_repo = ProductsRepository(session)

                cart = await cart_repo.get_cart_by_user_id(user_id)
                if not cart:
                    raise Exception("Cart not found")

                items = await cart_repo.get_cart_items(cart.id)
                if not items:
                    raise Exception("Cart is empty")

                total_price = 0

                for item in items:
                    product = await product_repo.get_product_by_id(item.product_id)

                    if product.stock < item.quantity:
                        raise Exception(f"Not enough stock for product {item.product_id}")

                    total_price += product.price * item.quantity

                    order_item = OrderItem(
                        order_id=order_id,
                        product_id=product.id,
                        quantity=item.quantity,
                        price=product.price,
                    )
                    await order_repo.create_order_item(order_item)

                await order_repo.update_total_price(order_id, total_price)

                await self.cart_service.clear_cart(user_id)

                print(f"[SUCCESS] Order {order_id} processed successfully")

            except Exception as e:
                await session.rollback()
                print(f"[ERROR] Failed to process order {order_id}: {type(e).__name__} - {e}")
                raise 


    async def get_user_orders(self, user_id: int):
        orders = await self.order_repo.get_orders_by_user(user_id)
        return orders

    async def get_order(self, order_id: int):
        order = await self.order_repo.get_order(order_id)
        return order
