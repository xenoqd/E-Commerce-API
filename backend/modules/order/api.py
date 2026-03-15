from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_user
from ..user.models import User

from .service import OrderService
from .dependencies import get_order_service

order_router = APIRouter(prefix="/order", tags=["Order"])


@order_router.post("/checkout")
async def checkout(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    order = await service.checkout(current_user.id)
    return order


@order_router.get("/")
async def get_orders(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    orders = await service.get_user_orders(current_user.id)
    return orders


@order_router.get("/{order_id}")
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    order = await service.get_order(order_id)
    return order
