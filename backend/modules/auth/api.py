from fastapi import APIRouter, Depends, Request, Response

from ...core.utils import get_client_ip
from ..user.schemas import UserCreate, UserOut, UserLogin
from .service import AuthService
from .dependencies import get_auth_service


auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", response_model=UserOut)
async def register(
    response: Response,
    user_in: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.register(user_in, response)
    return user


@auth_router.post("/login", response_model=UserOut)
async def login(
    request: Request,
    response: Response,
    user_in: UserLogin,
    service: AuthService = Depends(get_auth_service),
):
    ip = get_client_ip(request)
    user = await service.login(user_in, response, ip=ip)
    return user
