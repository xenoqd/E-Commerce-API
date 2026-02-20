from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_session
from .repository import UserRepository
from .service import UserService
from backend.core.event_bus import EventBus


def get_event_bus(request: Request) -> EventBus:
    return request.app.state.event_bus


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    event_bus: EventBus = Depends(get_event_bus),
):
    return UserService(repo=repo, event_bus=event_bus)