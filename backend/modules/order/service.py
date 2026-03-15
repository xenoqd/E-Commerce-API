from fastapi import HTTPException

from .model import Order, OrderItem
from .repository import OrderRepository

from ..products.repository import ProductsRepository
from ..cart.repository import CartRepository

from datetime import datetime, timedelta

class OrderService:
    def __init__(self, order_repo: OrderRepository, cart_repo: CartRepository, product_repo: ProductsRepository):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.product_repo = product_repo


    async def checkout(self, user_id: int):
        cart = await self.cart_repo.get_cart_by_user_id(user_id)

        if not cart:
            raise HTTPException(400, "Cart empty")

        items = await self.cart_repo.get_cart_items(cart.id)

        if not items:
            raise HTTPException(400, "Cart empty")

        total_price = 0

        order = Order(user_id=user_id, total_price=0, expires_at=datetime.utcnow() + timedelta(minutes=10))

        order = await self.order_repo.create_order(order)

        for item in items:

            product = await self.product_repo.get_product_by_id(item.product_id)

            if product.stock < item.quantity:
                raise HTTPException(400, "Not enough stock")

            item_total = product.price * item.quantity
            total_price += item_total

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )

            await self.order_repo.create_order_item(order_item)

        order.total_price = total_price

        await self.order_repo.update_order(order)

        await self.cart_repo.clear_cart(cart.id)

        return order

    async def get_user_orders(self, user_id: int):
        orders = await self.order_repo.get_orders_by_user(user_id)
        return orders

    async def get_order(self, order_id: int):
        order = await self.order_repo.get_order(order_id)
        return order