from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security.jwt import decode_access_token
from backend.db.session import get_session
from backend.core.event_bus import EventBus

from ..user.repository import UserRepository
from ..user.service import UserService
from .service import AuthService

from jwt import PyJWTError
from typing import Optional


def get_event_bus(request: Request) -> EventBus:
    return request.app.state.event_bus


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    event_bus: EventBus = Depends(get_event_bus),
):
    return UserService(repo=repo, event_bus=event_bus)


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
):
    return AuthService(user_service=user_service)


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_cookie: Optional[str] = request.cookies.get("access_token")
    if not auth_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_cookie

    try:
        payload = decode_access_token(token)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    repo = UserRepository(session)
    user = await repo.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


async def get_admin_user(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return current_user
