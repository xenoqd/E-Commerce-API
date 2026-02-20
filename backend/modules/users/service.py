from .repository import UserRepository

from backend.core.event_bus import EventBus
from .schemas import UserCreate
from .models import User
from backend.core.security.password import get_password_hash

class UserService:
    def __init__(self, repo: UserRepository, event_bus: EventBus):
        self.repo = repo
        self.event_bus = event_bus

    async def register(self, user_in: UserCreate):
        user = User(
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password)
        )
        await self.repo.create(user)

        await self.event_bus.publish(
            "user.registered",
            {"user_id": user.id, "username":user.username}
        )
        return user