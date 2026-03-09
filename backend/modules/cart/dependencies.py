from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_session
from .repository import CartRepository
from ..products.repository import ProductsRepository
from .service import CartService


async def get_cart_service(
    session: AsyncSession = Depends(get_session),
):
    cart_repo = CartRepository(session)
    product_repo = ProductsRepository(session)
    return CartService(cart_repo, product_repo)
