from backend.modules.order.repository import OrderRepository
from backend.modules.products.repository import ProductsRepository
from backend.modules.cart.repository import CartRepository
from backend.modules.cart.service import CartService
from backend.modules.order.model import OrderItem


class OrderHandlers:
    def __init__(
        self,
        order_repo: OrderRepository,
        cart_repo: CartRepository,
        product_repo: ProductsRepository,
        cart_service: CartService,
    ):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.product_repo = product_repo
        self.cart_service = cart_service

    async def handle_order_created(self, data: dict):
        order_id = data["order_id"]
        user_id = data["user_id"]

        print(f"[INFO] Start processing order_id={order_id} user_id={user_id}")

        cart = await self.cart_repo.get_cart_by_user_id(user_id)
        if not cart:
            raise Exception("Cart not found")

        items = await self.cart_repo.get_cart_items(cart.id)
        if not items:
            raise Exception("Cart is empty")

        total_price = 0

        for item in items:
            product = await self.product_repo.get_product_by_id(item.product_id)

            if product.stock < item.quantity:
                raise Exception("Not enough stock")

            item_total = product.price * item.quantity
            total_price += item_total

            order_item = OrderItem(
                order_id=order_id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price,
            )

            await self.order_repo.create_order_item(order_item)

        await self.order_repo.update_total_price(order_id, total_price)
        await self.cart_service.clear_cart(user_id)
