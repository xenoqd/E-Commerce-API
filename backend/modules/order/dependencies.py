from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_session

from backend.modules.products.repository import ProductsRepository
from backend.modules.order.repository import OrderRepository
from backend.modules.cart.repository import CartRepository
from backend.modules.order.service import OrderService

from backend.modules.cart.service import CartService


async def get_order_service(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    order_repo = OrderRepository(session)
    cart_repo = CartRepository(session)
    product_repo = ProductsRepository(session)

    event_bus = request.app.state.event_bus

    cart_service = CartService(cart_repo, product_repo, event_bus)

    return OrderService(order_repo, cart_repo, product_repo, cart_service, event_bus)
