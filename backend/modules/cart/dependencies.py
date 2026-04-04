from fastapi import Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_session
from backend.modules.cart.service import CartService
from backend.modules.cart.repository import CartRepository
from backend.modules.products.repository import ProductsRepository


async def get_cart_service(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    cart_repo = CartRepository(session)
    product_repo = ProductsRepository(session)
    event_bus = request.app.state.event_bus
    return CartService(cart_repo, product_repo, event_bus)
