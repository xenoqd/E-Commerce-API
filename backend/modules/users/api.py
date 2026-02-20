from fastapi import APIRouter, Depends

from .schemas import UserCreate
from .service import UserService
from .dependencies import get_user_service

register_router = APIRouter(prefix="/auth")


@register_router.post("/register")
async def register(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    user = await service.register(user_in)
    return user