from ..user.service import UserService
from ..user.schemas import UserCreate, UserLogin


from backend.core.security.jwt import create_access_token, create_refresh_token
from backend.core.config import settings

from fastapi import Response


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, user_in: UserCreate, response: Response):
        user = await self.user_service.create_user(user_in)

        access_token = create_access_token(
            {
                "sub": str(user.id),
            }
        )
        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/",
        )
        return user

    async def login(self, user_in: UserLogin, response: Response, ip: str = "unknown"):
        user = await self.user_service.login_user(user_in, ip=ip)

        access_token = create_access_token(
            {
                "sub": str(user.id),
            }
        )
        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/",
        )
        return user
