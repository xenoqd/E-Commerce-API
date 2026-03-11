from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_user
from ..user.models import User

from .schemas import AddToCart
from .dependencies import get_cart_service
from .service import CartService


cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.get("")
async def get_cart(
    service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    cart = await service.get_cart(
        user_id=current_user.id,
    )
    return cart


@cart_router.post("/items")
async def add_item_to_cart(
    data: AddToCart,
    service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    return await service.add_to_cart(
        user_id=current_user.id, 
        product_id=data.product_id
    )


@cart_router.delete("/items/{product_id}")
async def remove_item_from_cart(
    product_id: int,
    service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    return await service.remove_from_cart(
        user_id=current_user.id, 
        product_id=product_id
    )


@cart_router.delete("")
async def clear_cart(
    service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    cart = await service.clear_cart(user_id=current_user.id)
    return cart
