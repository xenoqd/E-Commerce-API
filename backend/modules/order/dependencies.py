from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_session
from .repository import OrderRepository

from ..products.repository import ProductsRepository
from ..products.repository import ProductsRepository
from ..cart.repository import CartRepository

from .service import OrderService


async def get_order_service(
    session: AsyncSession = Depends(get_session),
):
    order_repo = OrderRepository(session)
    product_repo = ProductsRepository(session)
    cart_repo = CartRepository(session)
    return OrderService(order_repo, cart_repo, product_repo)
